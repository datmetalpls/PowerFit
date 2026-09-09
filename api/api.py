"""API REST para gestionar socios y clases de PowerFit."""

from datetime import date
from datetime import timedelta
from decimal import Decimal
import hashlib
from typing import Dict, List, Literal

from fastapi import FastAPI, HTTPException, Query, status
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
    """Convierte una contraseña en un hash antes de guardarla."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


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


def obtener_trabajador_autorizado(idTrabajador: int, pass_: str) -> Trabajador:
    """Busca un trabajador por código y comprueba su contraseña."""
    trabajador = trabajadores.get(idTrabajador)
    if trabajador is None or not trabajador.autenticar(crear_hash(pass_)):
        raise HTTPException(status_code=401, detail="ID o contraseña incorrectos.")
    return trabajador


def exigir_rol(trabajador: Trabajador, rol: type) -> None:
    """Rechaza el acceso cuando el trabajador no tiene el rol requerido."""
    if not isinstance(trabajador, rol):
        raise HTTPException(status_code=403, detail="El trabajador no tiene este permiso.")


@app.get("/", tags=["Estado"])
def estado_api() -> dict:
    """Informa que la API está disponible."""
    return {"mensaje": "PowerFit API funcionando"}


@app.post("/socios", status_code=status.HTTP_201_CREATED, tags=["Socios"])
def crear_socio(datos: SocioEntrada) -> dict:
    """Registra un socio y le crea una membresía inicial de 30 días."""
    if datos.rut in socios:
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
        rut=datos.rut,
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
def listar_socios() -> list[dict]:
    """Devuelve todos los socios registrados."""
    return [convertir_socio_a_respuesta(socio) for socio in socios.values()]


@app.get("/socios/{rut}", tags=["Socios"])
def obtener_socio(rut: str) -> dict:
    """Devuelve un socio usando su RUT."""
    socio = socios.get(rut)
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado.")
    return convertir_socio_a_respuesta(socio)


@app.post("/socios/{rut}/ficha", tags=["Socios"])
def crear_ficha_socio(rut: str) -> dict:
    """Crea la ficha de seguimiento de un socio."""
    socio = socios.get(rut)
    if socio is None:
        raise HTTPException(status_code=404, detail="No existe un socio con ese rut.")
    socio.crearFicha()
    return {"rut": rut, "ficha": socio.ficha}


@app.post("/trabajadores", status_code=status.HTTP_201_CREATED, tags=["Trabajadores"])
def crear_trabajador(datos: TrabajadorEntrada) -> dict:
    """Registra un instructor o recepcionista con contraseña protegida."""
    if datos.codigo_trabajador in trabajadores:
        raise HTTPException(status_code=409, detail="El trabajador ya existe.")
    if any(trabajador.getRut() == datos.rut for trabajador in trabajadores.values()):
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
        "rut": datos.rut,
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
def listar_trabajadores() -> list[dict]:
    """Devuelve trabajadores sin incluir sus contraseñas."""
    return [convertir_trabajador_a_respuesta(trabajador) for trabajador in trabajadores.values()]


@app.post("/instructores/{codigo_trabajador}/clases/{codigo_clase}", tags=["Instructores"])
def asignar_clase(
    codigo_trabajador: int,
    codigo_clase: int,
    pass_: str = Query(..., alias="pass", min_length=1),
) -> dict:
    """Asigna una clase usando la contraseña del instructor."""
    trabajador = obtener_trabajador_autorizado(codigo_trabajador, pass_)
    exigir_rol(trabajador, Instructor)
    clase = clases.get(codigo_clase)
    if clase is None:
        raise HTTPException(status_code=404, detail="Clase no encontrada.")
    trabajador.dictarClase(clase)
    return convertir_clase_a_respuesta(clase)


@app.post("/instructores/{codigo_trabajador}/asistencias/{rut}", tags=["Instructores"])
def marcar_asistencia(
    codigo_trabajador: int,
    rut: str,
    pass_: str = Query(..., alias="pass", min_length=1),
) -> dict:
    """Registra asistencia usando la contraseña del instructor."""
    trabajador = obtener_trabajador_autorizado(codigo_trabajador, pass_)
    exigir_rol(trabajador, Instructor)
    if trabajador.idTrabajador != codigo_trabajador:
        raise HTTPException(status_code=403, detail="Solo puede operar su propio usuario.")
    socio = socios.get(rut)
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado.")
    trabajador.marcarAsistencia(socio)
    return {"mensaje": "Asistencia registrada.", "rut": rut}


@app.post("/recepcionistas/{codigo_trabajador}/socios/{rut}/activar", tags=["Recepcionistas"])
def activar_socio(
    codigo_trabajador: int,
    rut: str,
    pass_: str = Query(..., alias="pass", min_length=1),
) -> dict:
    """Activa un socio usando la contraseña del recepcionista."""
    trabajador = obtener_trabajador_autorizado(codigo_trabajador, pass_)
    exigir_rol(trabajador, Recepcionista)
    socio = socios.get(rut)
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado.")
    trabajador.registrarSocio(socio)
    return convertir_socio_a_respuesta(socio)


@app.post("/recepcionistas/{codigo_trabajador}/socios/{rut}/cobrar", tags=["Recepcionistas"])
def cobrar_mensualidad(
    codigo_trabajador: int,
    rut: str,
    pass_: str = Query(..., alias="pass", min_length=1),
) -> dict:
    """Registra un cobro usando la contraseña del recepcionista."""
    trabajador = obtener_trabajador_autorizado(codigo_trabajador, pass_)
    exigir_rol(trabajador, Recepcionista)
    socio = socios.get(rut)
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado.")
    trabajador.cobrarMensualidad(socio)
    return {"mensaje": "Mensualidad cobrada.", "rut": rut}


@app.post("/productos", status_code=status.HTTP_201_CREATED, tags=["Inventario"])
def crear_producto(datos: ProductoEntrada) -> dict:
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
def listar_inventario() -> list[dict]:
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
    codigo_trabajador: int = Query(..., description="Código del recepcionista."),
    pass_: str = Query(..., alias="pass", min_length=1),
) -> dict:
    """Registra una venta, valida stock y descuenta las unidades vendidas."""
    if datos.codigo_venta in ventas:
        raise HTTPException(status_code=409, detail="El codigo_venta ya está registrado.")

    trabajador = obtener_trabajador_autorizado(codigo_trabajador, pass_)
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
                "cantidad": detalle.cantidad,
                "precio_unitario_clp": detalle.precioUnitarioCLP,
                "subtotal_clp": detalle.subtotalCLP,
            }
            for detalle in venta.detalles
        ],
    }


@app.post("/clases", status_code=status.HTTP_201_CREATED, tags=["Clases"])
def crear_clase(datos: ClaseEntrada) -> dict:
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
def listar_clases() -> list[dict]:
    """Devuelve todas las clases creadas."""
    return [convertir_clase_a_respuesta(clase) for clase in clases.values()]


@app.post("/clases/{codigo_clase}/realizar", tags=["Clases"])
def realizar_clase(codigo_clase: int) -> dict:
    """Marca una clase como realizada si tiene socios inscritos."""
    clase = clases.get(codigo_clase)
    if clase is None:
        raise HTTPException(status_code=404, detail="No existe una clase con ese codigo_clase.")
    try:
        clase.realizarClase()
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error
    return convertir_clase_a_respuesta(clase)


@app.post("/clases/{codigo_clase}/inscripciones/{rut}", tags=["Clases"])
def inscribir_socio(codigo_clase: int, rut: str) -> dict:
    """Inscribe un socio activo con membresía vigente en una clase."""
    clase = clases.get(codigo_clase)
    socio = socios.get(rut)
    if clase is None:
        raise HTTPException(status_code=404, detail="Clase no encontrada.")
    if socio is None:
        raise HTTPException(status_code=404, detail="Socio no encontrado.")
    if not socio.estadoActivo:
        raise HTTPException(status_code=403, detail="El socio está inactivo.")
    if not socio.tieneMembresiaVigente():
        raise HTTPException(status_code=403, detail="El socio no tiene una membresía vigente.")
    if not clase.inscribirSocio(socio):
        raise HTTPException(status_code=409, detail="No hay cupo o el socio ya está inscrito.")
    return convertir_clase_a_respuesta(clase)
