"""API REST para gestionar socios y clases de PowerFit."""

from datetime import date, datetime, timedelta, timezone
from decimal import Decimal
import hashlib
import hmac
import os
import re
import secrets
from typing import Dict, List, Literal

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field

from clase_dirigida import ClaseDirigida
from crossfit import Crossfit
from direccion import Direccion
from membresia_mensual import MembresiaMensual
from instructor import Instructor
from inventario import Inventario
from recepcionista import Recepcionista
from socio import Socio
from spinning import Spinning
from suplemento import Suplemento
from trabajador import Trabajador
from venta import Venta
from detalle_venta import DetalleVenta
from yoga import Yoga


app = FastAPI(
    title="PowerFit API",
    description="API para administrar socios, membresías y clases dirigidas.",
    version="1.0.0",
)

socios: Dict[str, Socio] = {}
clases: Dict[int, ClaseDirigida] = {}
trabajadores: Dict[int, Trabajador] = {}
productos: Dict[int, Suplemento] = {}
inventarios: Dict[int, Inventario] = {}
ventas: Dict[int, Venta] = {}
sesiones: Dict[str, dict] = {}

seguridad_bearer = HTTPBearer(auto_error=False)
ADMIN_USUARIO = os.getenv("POWERFIT_ADMIN_USUARIO", "").strip()
ADMIN_PASSWORD = os.getenv("POWERFIT_ADMIN_PASSWORD", "")
DURACION_SESION = timedelta(hours=8)


class DireccionEntrada(BaseModel):
    """Datos necesarios para crear una dirección."""

    codigo_direccion: int = Field(gt=0, description="Código único de la dirección.")
    tipo_direccion: Literal["casa", "dpto", "block"] = Field(
        description="Tipo de dirección: casa, dpto o block."
    )
    calle: str = Field(min_length=1, description="Nombre de la calle.")
    numero_direccion: str = Field(min_length=1, description="Número de la calle.")
    referencia: str = Field(min_length=1, description="Referencia para ubicar el domicilio.")


class SocioEntrada(BaseModel):
    """Datos necesarios para registrar un socio."""

    rut: str = Field(
        min_length=2,
        description="RUT del socio, por ejemplo 12.345.678-5.",
    )
    edad: int = Field(ge=18, description="Edad del socio. Debe ser igual o mayor a 18.")
    nombres: str = Field(min_length=1, description="Nombres del socio.")
    apellido_paterno: str = Field(min_length=1, description="Apellido paterno del socio.")
    apellido_materno: str = Field(min_length=1, description="Apellido materno del socio.")
    telefono: str = Field(min_length=8, description="Teléfono de contacto del socio.")
    correo_electronico: str = Field(min_length=5, description="Correo electrónico del socio.")
    direccion: DireccionEntrada = Field(description="Domicilio del socio.")


class ClaseEntrada(BaseModel):
    """Datos comunes y específicos para crear una clase."""

    tipo_clase: Literal["yoga", "spinning", "crossfit"] = Field(
        description="Disciplina de la clase: yoga, spinning o crossfit."
    )
    codigo_clase: int = Field(gt=0, description="Código único de la clase.")
    nombre_clase: str = Field(min_length=1, description="Nombre de la clase.")
    cupo_maximo: int = Field(gt=0, description="Cantidad máxima de socios permitidos.")
    duracion_minutos: int = Field(gt=0, description="Duración de la clase en minutos.")
    nivel: str | None = Field(default=None, description="Nivel requerido para Yoga.")
    bicicletas_disponibles: int | None = Field(
        default=None, ge=0, description="Cantidad de bicicletas para Spinning."
    )
    estaciones_disponibles: int | None = Field(
        default=None, ge=0, description="Cantidad de estaciones para Crossfit."
    )


class TrabajadorEntrada(BaseModel):
    """Datos comunes y específicos para crear un trabajador."""

    tipo_trabajador: Literal["instructor", "recepcionista"] = Field(
        description="Rol del trabajador dentro del gimnasio."
    )
    pass_: str = Field(
        min_length=6,
        alias="pass",
        description="Contraseña del trabajador. Mínimo 6 caracteres.",
    )
    codigo_trabajador: int = Field(gt=0, description="Código único del trabajador.")
    rut: str = Field(
        min_length=2,
        description="RUT del trabajador, usado como identificador personal.",
    )
    edad: int = Field(ge=18, description="Edad del trabajador.")
    nombres: str = Field(min_length=1, description="Nombres del trabajador.")
    apellido_paterno: str = Field(min_length=1, description="Apellido paterno del trabajador.")
    apellido_materno: str = Field(min_length=1, description="Apellido materno del trabajador.")
    telefono: str = Field(min_length=8, description="Teléfono del trabajador.")
    correo_electronico: str = Field(min_length=5, description="Correo del trabajador.")
    direccion: DireccionEntrada = Field(description="Domicilio del trabajador.")
    especialidad: str | None = Field(default=None, description="Especialidad del instructor.")
    turno: str | None = Field(default=None, description="Turno del recepcionista.")


class ProductoEntrada(BaseModel):
    """Datos para registrar un suplemento en el inventario."""

    codigo_producto: int = Field(gt=0, description="Código único del suplemento.")
    nombre_producto: str = Field(min_length=1, description="Nombre del suplemento.")
    stock: int = Field(ge=0, description="Cantidad disponible del suplemento.")
    precio_usd: Decimal = Field(ge=0, description="Precio del suplemento en dólares.")


class DetalleVentaEntrada(BaseModel):
    """Producto y cantidad solicitados en una venta."""

    codigo_producto: int = Field(description="Código del producto que se venderá.")
    cantidad: int = Field(gt=0, description="Cantidad de unidades que se venderán.")


class VentaEntrada(BaseModel):
    """Datos necesarios para registrar una venta."""

    codigo_venta: int = Field(description="Código único de la venta.")
    valor_dolar_clp: Decimal = Field(
        gt=0, description="Valor actual de un dólar expresado en pesos chilenos."
    )
    detalles: list[DetalleVentaEntrada] = Field(
        min_length=1, description="Productos incluidos en la venta."
    )


class LoginEntrada(BaseModel):
    """Credenciales para iniciar una sesión protegida."""

    tipo_usuario: Literal["administrador", "trabajador"]
    usuario: str = Field(min_length=1, description="Usuario administrador o código del trabajador.")
    password: str = Field(min_length=6, description="Contraseña de acceso.")


def normalizar_rut(rut: str) -> str:
    """Devuelve el RUT en una forma única para almacenar y buscar."""
    return re.sub(r"[.\-\s]", "", rut).upper()


def convertir_socio_a_respuesta(socio: Socio) -> dict:
    """Convierte un socio del dominio a un diccionario JSON."""
    direccion = socio.getDireccion()
    return {
        "rut": socio.getRut(),
        "edad": socio.getEdad(),
        "nombres": socio.getNombres(),
        "apellido_paterno": socio.getApellidoPaterno(),
        "apellido_materno": socio.getApellidoMaterno(),
        "telefono": socio.getTelefono(),
        "correo_electronico": socio.getCorreoElectronico(),
        "telefono_valido": socio.validarTelefono(),
        "correo_valido": socio.validarCorreoElectronico(),
        "estado_activo": socio.estadoActivo,
        "membresia_vigente": socio.tieneMembresiaVigente(),
        "direccion": {
            "codigo_direccion": direccion.getIdDireccion(),
            "tipo_direccion": direccion.getTipoDireccion(),
            "calle": direccion.getCalle(),
            "numero_direccion": direccion.getNumero(),
            "referencia": direccion.getReferencia(),
        },
    }


def convertir_clase_a_respuesta(clase: ClaseDirigida) -> dict:
    """Convierte una clase del dominio a un diccionario JSON."""
    return {
        "codigo_clase": clase.codigo,
        "nombre_clase": clase.nombre,
        "tipo_clase": clase.__class__.__name__,
        "cupo_maximo": clase.cupoMaximo,
        "cupos_disponibles": clase.calcularCuposDisponibles(),
        "duracion_minutos": clase.duracionMinutos,
        "realizada": clase.realizada,
        "socios_inscritos": [socio.getRut() for socio in clase.socios],
    }


def convertir_trabajador_a_respuesta(trabajador: Trabajador) -> dict:
    """Convierte un trabajador sin exponer su contraseña."""
    respuesta = {
        "tipo_trabajador": trabajador.__class__.__name__.lower(),
        "codigo_trabajador": trabajador.idTrabajador,
        "rut": trabajador.getRut(),
        "nombres": trabajador.getNombres(),
        "apellido_paterno": trabajador.getApellidoPaterno(),
        "apellido_materno": trabajador.getApellidoMaterno(),
        "correo_electronico": trabajador.getCorreoElectronico(),
    }
    if isinstance(trabajador, Instructor):
        respuesta["especialidad"] = trabajador.especialidad
    if isinstance(trabajador, Recepcionista):
        respuesta["turno"] = trabajador.turno
    return respuesta


def crear_hash(password: str) -> str:
    """Protege una contraseña con PBKDF2, sal aleatoria y múltiples iteraciones."""
    iteraciones = 600_000
    sal = secrets.token_bytes(16)
    resumen = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), sal, iteraciones)
    return f"pbkdf2_sha256${iteraciones}${sal.hex()}${resumen.hex()}"


def verificar_password(password: str, hash_guardado: str) -> bool:
    """Comprueba una contraseña sin realizar comparaciones vulnerables a temporización."""
    try:
        algoritmo, iteraciones, sal, resumen = hash_guardado.split("$", 3)
        if algoritmo != "pbkdf2_sha256":
            return False
        calculado = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(sal),
            int(iteraciones),
        ).hex()
        return hmac.compare_digest(calculado, resumen)
    except (TypeError, ValueError):
        return False


def validar_datos_persona(persona: Socio | Trabajador) -> None:
    """Valida los datos comunes y entrega errores claros para la API."""
    if not persona.validarRut():
        raise HTTPException(status_code=422, detail="El campo rut no contiene un RUT válido.")
    if not persona.validarTelefono():
        raise HTTPException(status_code=422, detail="El campo telefono no tiene un formato válido.")
    if not persona.validarCorreoElectronico():
        raise HTTPException(
            status_code=422,
            detail="El campo correo_electronico no tiene un formato válido.",
        )


def exigir_rol(trabajador: Trabajador, rol: type) -> None:
    """Rechaza el acceso cuando el trabajador no tiene el rol requerido."""
    if not isinstance(trabajador, rol):
        raise HTTPException(status_code=403, detail="El trabajador no tiene este permiso.")


def crear_sesion(rol: str, codigo_trabajador: int | None = None) -> tuple[str, datetime]:
    """Crea un token opaco temporal y guarda únicamente sus datos de autorización."""
    token = secrets.token_urlsafe(32)
    expira = datetime.now(timezone.utc) + DURACION_SESION
    sesiones[token] = {
        "rol": rol,
        "codigo_trabajador": codigo_trabajador,
        "expira": expira,
    }
    return token, expira


def obtener_sesion_actual(
    credenciales: HTTPAuthorizationCredentials | None = Depends(seguridad_bearer),
) -> dict:
    """Valida el token Bearer recibido en la cabecera Authorization."""
    if credenciales is None:
        raise HTTPException(status_code=401, detail="Se requiere autenticación.")
    sesion = sesiones.get(credenciales.credentials)
    if sesion is None or sesion["expira"] <= datetime.now(timezone.utc):
        sesiones.pop(credenciales.credentials, None)
        raise HTTPException(status_code=401, detail="La sesión no existe o expiró.")
    return sesion


def exigir_roles(*roles_permitidos: str):
    """Construye una dependencia que limita una ruta a determinados roles."""

    def validar(sesion: dict = Depends(obtener_sesion_actual)) -> dict:
        if sesion["rol"] not in roles_permitidos:
            raise HTTPException(status_code=403, detail="No tiene permiso para esta operación.")
        return sesion

    return validar


def exigir_identidad_trabajador(sesion: dict, codigo_trabajador: int) -> None:
    """Impide que un trabajador opere usando el código de otro trabajador."""
    if sesion["rol"] != "administrador" and sesion["codigo_trabajador"] != codigo_trabajador:
        raise HTTPException(status_code=403, detail="No puede operar con otro usuario.")


@app.get("/", tags=["Estado"])
def estado_api() -> dict:
    """Informa que la API está disponible."""
    return {"mensaje": "PowerFit API funcionando"}


@app.post("/auth/login", tags=["Autenticación"])
def iniciar_sesion(datos: LoginEntrada) -> dict:
    """Autentica al administrador o a un trabajador y entrega un token temporal."""
    if datos.tipo_usuario == "administrador":
        if not ADMIN_USUARIO or not ADMIN_PASSWORD:
            raise HTTPException(
                status_code=503,
                detail="El administrador inicial no está configurado en el servidor.",
            )
        credenciales_validas = hmac.compare_digest(
            datos.usuario, ADMIN_USUARIO
        ) and hmac.compare_digest(datos.password, ADMIN_PASSWORD)
        if not credenciales_validas:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas.")
        token, expira = crear_sesion("administrador")
    else:
        try:
            codigo_trabajador = int(datos.usuario)
        except ValueError as error:
            raise HTTPException(status_code=401, detail="Credenciales incorrectas.") from error
        trabajador = trabajadores.get(codigo_trabajador)
        if trabajador is None or not verificar_password(datos.password, trabajador.passHash):
            raise HTTPException(status_code=401, detail="Credenciales incorrectas.")
        rol = "instructor" if isinstance(trabajador, Instructor) else "recepcionista"
        token, expira = crear_sesion(rol, trabajador.idTrabajador)

    return {
        "access_token": token,
        "token_type": "bearer",
        "expira": expira,
    }


@app.post("/auth/logout", tags=["Autenticación"])
def cerrar_sesion(
    credenciales: HTTPAuthorizationCredentials = Depends(seguridad_bearer),
    _: dict = Depends(obtener_sesion_actual),
) -> dict:
    """Invalida el token utilizado en la solicitud."""
    sesiones.pop(credenciales.credentials, None)
    return {"mensaje": "Sesión cerrada."}


@app.post("/socios", status_code=status.HTTP_201_CREATED, tags=["Socios"])
def crear_socio(
    datos: SocioEntrada,
    _: dict = Depends(exigir_roles("administrador", "recepcionista")),
) -> dict:
    """Registra un socio y le crea una membresía inicial de 30 días."""
    rut = normalizar_rut(datos.rut)
    if rut in socios:
        raise HTTPException(status_code=409, detail="El socio ya está registrado.")

    direccion = Direccion(
        idDireccion=datos.direccion.codigo_direccion,
        tipoDireccion=datos.direccion.tipo_direccion,
        calle=datos.direccion.calle,
        numero=datos.direccion.numero_direccion,
        referencia=datos.direccion.referencia,
    )
    socio = Socio(
        estadoActivo=True,
        rut=rut,
        edad=datos.edad,
        nombres=datos.nombres,
        apellidoPaterno=datos.apellido_paterno,
        apellidoMaterno=datos.apellido_materno,
        telefono=datos.telefono,
        correoElectronico=datos.correo_electronico,
        direccion=direccion,
    )

    validar_datos_persona(socio)

    hoy = date.today()
    socio.membresias.append(MembresiaMensual(hoy, hoy + timedelta(days=30)))
    socios[socio.getRut()] = socio
    return convertir_socio_a_respuesta(socio)


@app.get("/socios", response_model=List[dict], tags=["Socios"])
def listar_socios(
    _: dict = Depends(exigir_roles("administrador", "recepcionista")),
) -> list[dict]:
    """Devuelve todos los socios registrados."""
    return [convertir_socio_a_respuesta(socio) for socio in socios.values()]


@app.get("/socios/{rut}", tags=["Socios"])
def obtener_socio(
    rut: str,
    _: dict = Depends(exigir_roles("administrador", "recepcionista")),
) -> dict:
    """Devuelve un socio usando su RUT."""
    socio = socios.get(normalizar_rut(rut))
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado.")
    return convertir_socio_a_respuesta(socio)


@app.post("/socios/{rut}/ficha", tags=["Socios"])
def crear_ficha_socio(
    rut: str,
    _: dict = Depends(exigir_roles("administrador", "recepcionista")),
) -> dict:
    """Crea la ficha de seguimiento de un socio."""
    socio = socios.get(normalizar_rut(rut))
    if socio is None:
        raise HTTPException(status_code=404, detail="No existe un socio con ese rut.")
    socio.crearFicha()
    return {"rut": rut, "ficha": socio.ficha}


@app.post("/trabajadores", status_code=status.HTTP_201_CREATED, tags=["Trabajadores"])
def crear_trabajador(
    datos: TrabajadorEntrada,
    _: dict = Depends(exigir_roles("administrador")),
) -> dict:
    """Registra un instructor o recepcionista con contraseña protegida."""
    if datos.codigo_trabajador in trabajadores:
        raise HTTPException(status_code=409, detail="El trabajador ya existe.")
    rut = normalizar_rut(datos.rut)
    if any(trabajador.getRut() == rut for trabajador in trabajadores.values()):
        raise HTTPException(status_code=409, detail="El rut del trabajador ya está registrado.")

    direccion = Direccion(
        idDireccion=datos.direccion.codigo_direccion,
        tipoDireccion=datos.direccion.tipo_direccion,
        calle=datos.direccion.calle,
        numero=datos.direccion.numero_direccion,
        referencia=datos.direccion.referencia,
    )
    datos_persona = {
        "idTrabajador": datos.codigo_trabajador,
        "passHash": crear_hash(datos.pass_),
        "rut": rut,
        "edad": datos.edad,
        "nombres": datos.nombres,
        "apellidoPaterno": datos.apellido_paterno,
        "apellidoMaterno": datos.apellido_materno,
        "telefono": datos.telefono,
        "correoElectronico": datos.correo_electronico,
        "direccion": direccion,
    }

    if datos.tipo_trabajador == "instructor":
        if not datos.especialidad:
            raise HTTPException(status_code=422, detail="Instructor requiere especialidad.")
        trabajador = Instructor(especialidad=datos.especialidad, **datos_persona)
        trabajador.permisos.update({"dictar_clase", "marcar_asistencia"})
    else:
        if not datos.turno:
            raise HTTPException(status_code=422, detail="Recepcionista requiere turno.")
        trabajador = Recepcionista(turno=datos.turno, **datos_persona)
        trabajador.permisos.update({"registrar_socio", "cobrar_mensualidad"})

    validar_datos_persona(trabajador)

    trabajadores[trabajador.idTrabajador] = trabajador
    return convertir_trabajador_a_respuesta(trabajador)


@app.get("/trabajadores", response_model=List[dict], tags=["Trabajadores"])
def listar_trabajadores(
    _: dict = Depends(exigir_roles("administrador")),
) -> list[dict]:
    """Devuelve trabajadores sin incluir sus contraseñas."""
    return [convertir_trabajador_a_respuesta(trabajador) for trabajador in trabajadores.values()]


@app.post("/instructores/{codigo_trabajador}/clases/{codigo_clase}", tags=["Instructores"])
def asignar_clase(
    codigo_trabajador: int,
    codigo_clase: int,
    _: dict = Depends(exigir_roles("administrador")),
) -> dict:
    """Permite al administrador asignar una clase a un instructor."""
    trabajador = trabajadores.get(codigo_trabajador)
    if trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado.")
    exigir_rol(trabajador, Instructor)
    clase = clases.get(codigo_clase)
    if clase is None:
        raise HTTPException(status_code=404, detail="Clase no encontrada.")
    trabajador.dictarClase(clase)
    return convertir_clase_a_respuesta(clase)


@app.post(
    "/instructores/{codigo_trabajador}/asistencias/{codigo_clase}/{rut}",
    tags=["Instructores"],
)
def marcar_asistencia(
    codigo_trabajador: int,
    codigo_clase: int,
    rut: str,
    sesion: dict = Depends(exigir_roles("instructor")),
) -> dict:
    """Registra asistencia usando la sesión del instructor responsable."""
    exigir_identidad_trabajador(sesion, codigo_trabajador)
    trabajador = trabajadores.get(codigo_trabajador)
    if trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado.")
    exigir_rol(trabajador, Instructor)
    clase = clases.get(codigo_clase)
    if clase is None:
        raise HTTPException(status_code=404, detail="Clase no encontrada.")
    if getattr(clase, "instructor", None) is not trabajador:
        raise HTTPException(status_code=403, detail="El instructor no dicta esta clase.")
    if clase.realizada:
        raise HTTPException(status_code=409, detail="La clase ya fue realizada.")
    socio = socios.get(normalizar_rut(rut))
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado.")
    if socio not in clase.socios:
        raise HTTPException(status_code=409, detail="El socio no está inscrito en esta clase.")
    if not socio.tieneMembresiaVigente():
        raise HTTPException(status_code=403, detail="El socio no tiene una membresía vigente.")
    trabajador.marcarAsistencia(socio, clase)
    return {"mensaje": "Asistencia registrada.", "rut": socio.getRut(), "codigo_clase": codigo_clase}


@app.post("/recepcionistas/{codigo_trabajador}/socios/{rut}/activar", tags=["Recepcionistas"])
def activar_socio(
    codigo_trabajador: int,
    rut: str,
    sesion: dict = Depends(exigir_roles("administrador", "recepcionista")),
) -> dict:
    """Activa un socio usando una sesión autorizada."""
    exigir_identidad_trabajador(sesion, codigo_trabajador)
    trabajador = trabajadores.get(codigo_trabajador)
    if trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado.")
    exigir_rol(trabajador, Recepcionista)
    socio = socios.get(normalizar_rut(rut))
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado.")
    trabajador.registrarSocio(socio)
    return convertir_socio_a_respuesta(socio)


@app.post("/recepcionistas/{codigo_trabajador}/socios/{rut}/cobrar", tags=["Recepcionistas"])
def cobrar_mensualidad(
    codigo_trabajador: int,
    rut: str,
    sesion: dict = Depends(exigir_roles("administrador", "recepcionista")),
) -> dict:
    """Registra un cobro usando una sesión autorizada."""
    exigir_identidad_trabajador(sesion, codigo_trabajador)
    trabajador = trabajadores.get(codigo_trabajador)
    if trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado.")
    exigir_rol(trabajador, Recepcionista)
    socio = socios.get(normalizar_rut(rut))
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado.")
    try:
        trabajador.cobrarMensualidad(socio)
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return {"mensaje": "Mensualidad cobrada.", "rut": socio.getRut()}


@app.post("/productos", status_code=status.HTTP_201_CREATED, tags=["Inventario"])
def crear_producto(
    datos: ProductoEntrada,
    _: dict = Depends(exigir_roles("administrador", "recepcionista")),
) -> dict:
    """Registra un suplemento y crea su control de inventario."""
    if datos.codigo_producto in productos:
        raise HTTPException(
            status_code=409,
            detail="Ya existe un producto con ese codigo_producto.",
        )

    producto = Suplemento(
        codigo=datos.codigo_producto,
        nombre=datos.nombre_producto,
        stock=datos.stock,
        precioUSD=datos.precio_usd,
    )
    productos[producto.codigo] = producto
    inventarios[producto.codigo] = Inventario(
        fechaActualizacion=date.today(),
        stockMinimo=1,
        stockActual=producto.stock,
    )
    return {
        "codigo_producto": producto.codigo,
        "nombre_producto": producto.nombre,
        "stock_actual": producto.stock,
        "precio_usd": producto.precioUSD,
    }


@app.get("/inventario", tags=["Inventario"])
def listar_inventario(
    _: dict = Depends(exigir_roles("administrador", "recepcionista")),
) -> list[dict]:
    """Devuelve existencias y alertas de todos los productos."""
    return [
        {
            "codigo_producto": codigo_producto,
            "stock_actual": inventario.stockActual,
            "stock_minimo": inventario.stockMinimo,
            "alerta_stock": inventario.alertaStock(),
            "fecha_actualizacion": inventario.fechaActualizacion,
        }
        for codigo_producto, inventario in inventarios.items()
    ]


@app.post("/ventas", status_code=status.HTTP_201_CREATED, tags=["Ventas"])
def registrar_venta(
    datos: VentaEntrada,
    codigo_trabajador: int,
    sesion: dict = Depends(exigir_roles("administrador", "recepcionista")),
) -> dict:
    """Registra una venta, valida stock y descuenta las unidades vendidas."""
    if datos.codigo_venta in ventas:
        raise HTTPException(status_code=409, detail="El codigo_venta ya está registrado.")

    exigir_identidad_trabajador(sesion, codigo_trabajador)
    trabajador = trabajadores.get(codigo_trabajador)
    if trabajador is None:
        raise HTTPException(status_code=404, detail="Trabajador no encontrado.")
    exigir_rol(trabajador, Recepcionista)
    venta = Venta(numero=datos.codigo_venta, fecha=date.today())

    cantidades_por_producto: dict[int, int] = {}
    for entrada in datos.detalles:
        cantidades_por_producto[entrada.codigo_producto] = (
            cantidades_por_producto.get(entrada.codigo_producto, 0)
            + entrada.cantidad
        )

    for codigo_producto, cantidad_total in cantidades_por_producto.items():
        producto = productos.get(codigo_producto)
        if producto is None:
            raise HTTPException(
                status_code=404,
                detail=f"No existe el codigo_producto {codigo_producto}.",
            )
        if producto.stock < cantidad_total:
            raise HTTPException(
                status_code=409,
                detail=(
                    f"Stock insuficiente para codigo_producto {codigo_producto}. "
                    f"Solicitado: {cantidad_total}. Disponible: {producto.stock}."
                ),
            )

    for entrada in datos.detalles:
        producto = productos.get(entrada.codigo_producto)
        precio_clp = producto.calcularPrecioCLP(datos.valor_dolar_clp)
        detalle = DetalleVenta(
            codigoProducto=producto.codigo,
            cantidad=entrada.cantidad,
            precioUnitarioCLP=precio_clp,
            stock=producto.stock,
        )
        if not venta.agregarDetalle(detalle):
            raise HTTPException(status_code=409, detail="No se pudo agregar el detalle de venta.")

    if not trabajador.registrarVenta(venta):
        raise HTTPException(status_code=409, detail="La venta no contiene detalles válidos.")

    for codigo_producto, cantidad_total in cantidades_por_producto.items():
        producto = productos[codigo_producto]
        producto.descontarStock(cantidad_total)
        inventarios[producto.codigo].stockActual = producto.stock
        inventarios[producto.codigo].fechaActualizacion = date.today()

    ventas[venta.numero] = venta
    return {
        "codigo_venta": venta.numero,
        "fecha_venta": venta.fecha,
        "total_clp": venta.totalCLP,
        "detalles": [
            {
                "codigo_producto": detalle.codigoProducto,
                "cantidad": detalle.cantidad,
                "precio_unitario_clp": detalle.precioUnitarioCLP,
                "subtotal_clp": detalle.subtotalCLP,
            }
            for detalle in venta.detalles
        ],
    }


@app.post("/clases", status_code=status.HTTP_201_CREATED, tags=["Clases"])
def crear_clase(
    datos: ClaseEntrada,
    _: dict = Depends(exigir_roles("administrador")),
) -> dict:
    """Crea una clase de Yoga, Spinning o Crossfit."""
    if datos.codigo_clase in clases:
        raise HTTPException(status_code=409, detail="El código de clase ya existe.")

    if datos.tipo_clase == "yoga":
        if not datos.nivel:
            raise HTTPException(status_code=422, detail="Yoga requiere un nivel.")
        clase = Yoga(
            nivel=datos.nivel,
            codigo=datos.codigo_clase,
            nombre=datos.nombre_clase,
            cupoMaximo=datos.cupo_maximo,
            duracionMinutos=datos.duracion_minutos,
        )
    elif datos.tipo_clase == "spinning":
        if datos.bicicletas_disponibles is None:
            raise HTTPException(status_code=422, detail="Spinning requiere bicicletas.")
        clase = Spinning(
            bicicletasDisponibles=datos.bicicletas_disponibles,
            codigo=datos.codigo_clase,
            nombre=datos.nombre_clase,
            cupoMaximo=datos.cupo_maximo,
            duracionMinutos=datos.duracion_minutos,
        )
    else:
        if datos.estaciones_disponibles is None:
            raise HTTPException(status_code=422, detail="Crossfit requiere estaciones.")
        clase = Crossfit(
            estacionesDisponibles=datos.estaciones_disponibles,
            codigo=datos.codigo_clase,
            nombre=datos.nombre_clase,
            cupoMaximo=datos.cupo_maximo,
            duracionMinutos=datos.duracion_minutos,
        )

    clases[clase.codigo] = clase
    return convertir_clase_a_respuesta(clase)


@app.get("/clases", response_model=List[dict], tags=["Clases"])
def listar_clases(
    _: dict = Depends(exigir_roles("administrador", "recepcionista", "instructor")),
) -> list[dict]:
    """Devuelve todas las clases creadas."""
    return [convertir_clase_a_respuesta(clase) for clase in clases.values()]


@app.post("/clases/{codigo_clase}/realizar", tags=["Clases"])
def realizar_clase(
    codigo_clase: int,
    sesion: dict = Depends(exigir_roles("administrador", "instructor")),
) -> dict:
    """Marca una clase como realizada si tiene socios inscritos."""
    clase = clases.get(codigo_clase)
    if clase is None:
        raise HTTPException(status_code=404, detail="No existe una clase con ese codigo_clase.")
    if sesion["rol"] == "instructor":
        instructor = getattr(clase, "instructor", None)
        if instructor is None or instructor.idTrabajador != sesion["codigo_trabajador"]:
            raise HTTPException(status_code=403, detail="El instructor no dicta esta clase.")
    try:
        clase.realizarClase()
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return convertir_clase_a_respuesta(clase)


@app.post("/clases/{codigo_clase}/inscripciones/{rut}", tags=["Clases"])
def inscribir_socio(
    codigo_clase: int,
    rut: str,
    _: dict = Depends(exigir_roles("administrador", "recepcionista")),
) -> dict:
    """Inscribe un socio activo con membresía vigente en una clase."""
    clase = clases.get(codigo_clase)
    socio = socios.get(normalizar_rut(rut))
    if clase is None:
        raise HTTPException(status_code=404, detail="Clase no encontrada.")
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado.")
    if not socio.estadoActivo:
        raise HTTPException(status_code=403, detail="El socio está inactivo.")
    if clase.realizada:
        raise HTTPException(status_code=409, detail="No se puede inscribir en una clase ya realizada.")
    if not socio.tieneMembresiaVigente():
        raise HTTPException(status_code=403, detail="El socio no tiene una membresía vigente.")
    if not clase.inscribirSocio(socio):
        raise HTTPException(status_code=409, detail="No hay cupo o el socio ya está inscrito.")
    return convertir_clase_a_respuesta(clase)
