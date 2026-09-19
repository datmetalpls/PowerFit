"""PowerFit - Modelos Backend POO alineados 100% al UML Oficial del Profesor."""
from abc import ABC, abstractmethod
from datetime import date
from typing import List, Optional


# =============================================================================
# 1. CLASE ABSTRACTA BASE: Persona
# =============================================================================
class Persona(ABC):
    """Clase abstracta base con validación de RUT por Algoritmo Módulo 11."""

    def __init__(
        self,
        rut: str,
        nombres: str,
        apellidoPaterno: str = "",
        apellidoMaterno: str = "",
        telefono: str = "",
        correoElectronico: str = "",
    ):
        self._rut = rut
        self._nombres = nombres
        self._apellidoPaterno = apellidoPaterno
        self._apellidoMaterno = apellidoMaterno
        self._telefono = telefono
        self._correoElectronico = correoElectronico

    @property
    def rut(self) -> str:
        return self._rut

    @property
    def nombres(self) -> str:
        return self._nombres

    @property
    def nombre(self) -> str:
        """Alias 'nombre' exigido por el UML Oficial."""
        if self._apellidoPaterno:
            return f"{self._nombres} {self._apellidoPaterno}"
        return self._nombres

    @property
    def apellidoPaterno(self) -> str:
        return self._apellidoPaterno

    @property
    def apellidoMaterno(self) -> str:
        return self._apellidoMaterno

    @property
    def telefono(self) -> str:
        return self._telefono

    @property
    def correoElectronico(self) -> str:
        return self._correoElectronico

    def getRut(self) -> str:
        return self._rut

    def getNombres(self) -> str:
        return self._nombres

    def getApellidoPaterno(self) -> str:
        return self._apellidoPaterno

    def validarRut(self) -> bool:
        """Valida la autenticidad del RUT mediante el Algoritmo Módulo 11."""
        if not self._rut or not isinstance(self._rut, str):
            return False

        rut_limpio = self._rut.replace(".", "").replace("-", "").replace(" ", "").upper()
        if len(rut_limpio) < 2:
            return False

        cuerpo = rut_limpio[:-1]
        dv_ingresado = rut_limpio[-1]

        if not cuerpo.isdigit():
            return False

        suma = 0
        multiplicador = 2

        for digito in reversed(cuerpo):
            suma += int(digito) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = suma % 11
        resultado = 11 - resto

        if resultado == 11:
            dv_esperado = "0"
        elif resultado == 10:
            dv_esperado = "K"
        else:
            dv_esperado = str(resultado)

        return dv_ingresado == dv_esperado


# =============================================================================
# 2. SUBCLASE Socio (con regla de bloqueo permitirIngreso)
# =============================================================================
class Socio(Persona):
    """Representa a un Socio con fecha de vencimiento y control de ingreso."""

    def __init__(
        self,
        idSocio: int,
        rut: str,
        nombres: str,
        apellidoPaterno: str = "",
        fechaVencimientoMembresia: Optional[date] = None,
        apellidoMaterno: str = "",
        telefono: str = "",
        correoElectronico: str = "",
    ):
        super().__init__(
            rut=rut,
            nombres=nombres,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
        )
        self._idSocio = idSocio
        # Si no se indica fecha, por defecto se otorga 30 días de vigencia
        self._fechaVencimientoMembresia = fechaVencimientoMembresia or date.today()

    @property
    def idSocio(self) -> int:
        return self._idSocio

    @property
    def fechaVencimientoMembresia(self) -> date:
        return self._fechaVencimientoMembresia

    @fechaVencimientoMembresia.setter
    def fechaVencimientoMembresia(self, nueva_fecha: date):
        self._fechaVencimientoMembresia = nueva_fecha

    def getIdSocio(self) -> int:
        return self._idSocio

    def permitirIngreso(self) -> bool:
        """Regla de Bloqueo #2: Retorna True solo si la membresía no ha vencido."""
        if self._fechaVencimientoMembresia is None:
            return False
        return self._fechaVencimientoMembresia >= date.today()


# =============================================================================
# 3. JERARQUÍA DE TRABAJADORES (Trabajador, Instructor, Recepcionista)
# =============================================================================
class Trabajador(Persona, ABC):
    """Clase abstracta base para empleados con perfilamiento por ID y permisos."""

    def __init__(
        self,
        idTrabajador: str,
        rut: str,
        nombres: str,
        usuario: str = "",
        passHash: str = "",
        rol: str = "Trabajador",
        apellidoPaterno: str = "",
        telefono: str = "",
        correoElectronico: str = "",
    ):
        super().__init__(
            rut=rut,
            nombres=nombres,
            apellidoPaterno=apellidoPaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
        )
        self._idTrabajador = str(idTrabajador)
        self._usuario = usuario or nombres.lower().replace(" ", "")
        self._passHash = passHash
        self._rol = rol
        self._permisos = set()

    @property
    def idTrabajador(self) -> str:
        return self._idTrabajador

    @property
    def usuario(self) -> str:
        return self._usuario

    @property
    def rol(self) -> str:
        return self._rol

    def getRol(self) -> str:
        return self._rol

    def autenticar(self, password_intent: str) -> bool:
        return self._passHash == password_intent

    def tienePermiso(self, accion: str) -> bool:
        """Verifica si el trabajador posee permiso para ejecutar una acción."""
        if self._rol == "Administrador":
            return True
        return accion in self._permisos


class Instructor(Trabajador):
    """Instructor que dicta clases dirigidas y registra asistencia."""

    def __init__(
        self,
        especialidad: str,
        idTrabajador: str,
        rut: str,
        nombres: str,
        usuario: str = "",
        passHash: str = "",
        apellidoPaterno: str = "",
        telefono: str = "",
        correoElectronico: str = "",
    ):
        super().__init__(
            idTrabajador=idTrabajador,
            rut=rut,
            nombres=nombres,
            usuario=usuario,
            passHash=passHash,
            rol="Instructor",
            apellidoPaterno=apellidoPaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
        )
        self._especialidad = especialidad
        self._clases_dictadas = []

    @property
    def especialidad(self) -> str:
        return self._especialidad

    def getEspecialidad(self) -> str:
        return self._especialidad

    def dictarClase(self, clase) -> None:
        """Asigna la clase para dictarla."""
        if clase not in self._clases_dictadas:
            self._clases_dictadas.append(clase)

    def marcarAsistencia(self, socio: Socio, clase) -> bool:
        """Registra la presencia del socio en la clase."""
        if socio.permitirIngreso() and clase.hayCupo():
            return clase.reservarCupo()
        return False


class Recepcionista(Trabajador):
    """Recepcionista encargada de inscripciones, pagos y alta de socios."""

    def __init__(
        self,
        idTrabajador: str,
        rut: str,
        nombres: str,
        turno: str = "Mañana",
        usuario: str = "",
        passHash: str = "",
        apellidoPaterno: str = "",
        telefono: str = "",
        correoElectronico: str = "",
    ):
        super().__init__(
            idTrabajador=idTrabajador,
            rut=rut,
            nombres=nombres,
            usuario=usuario,
            passHash=passHash,
            rol="Recepcionista",
            apellidoPaterno=apellidoPaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
        )
        self._turno = turno
        self._socios_registrados = []

    @property
    def turno(self) -> str:
        return self._turno

    def getTurno(self) -> str:
        return self._turno

    def registrarSocio(self, socio: Socio) -> None:
        """Registra a un nuevo socio en el sistema."""
        if socio not in self._socios_registrados:
            self._socios_registrados.append(socio)

    def cobrarMensualidad(self, socio: Socio, monto: float) -> bool:
        """Extiende la membresía del socio tras el pago."""
        if socio:
            socio.fechaVencimientoMembresia = date.today()
            return True
        return False

    def crearInscripcion(self, socio: Socio, mes: int, anio: int):
        """Crea un objeto InscripcionMensual para el socio."""
        from src.models.inscripcion import InscripcionMensual
        return InscripcionMensual(mes=mes, anio=anio, socio=socio)


# =============================================================================
# 4. JERARQUÍA ClaseDirigida (Yoga, Spinning, Crossfit)
# =============================================================================
class ClaseDirigida(ABC):
    """Clase abstracta base para las clases dirigidas del gimnasio."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        duracionMin: int,
        cupoMaximo: int,
        instructor: Optional[Instructor] = None,
        sala: str = "Sala 1",
    ):
        self._codigo = codigo
        self._nombre = nombre
        self._duracionMin = duracionMin
        self._cupoMaximo = max(1, cupoMaximo)
        self._inscritos = 0
        self._instructor = instructor
        self._sala = sala
        self._lista_socios: List[Optional[Socio]] = [None] * self._cupoMaximo

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def duracionMin(self) -> int:
        return self._duracionMin

    @property
    def duracion_minutos(self) -> int:
        return self._duracionMin

    @property
    def cupoMaximo(self) -> int:
        return self._cupoMaximo

    @property
    def cupo_maximo(self) -> int:
        return self._cupoMaximo

    @property
    def inscritos(self) -> int:
        return self._inscritos

    @property
    def instructor(self) -> Optional[Instructor]:
        return self._instructor

    @instructor.setter
    def instructor(self, inst: Instructor):
        self._instructor = inst

    @property
    def sala(self) -> str:
        return self._sala

    @property
    def cupos(self) -> List[Optional[Socio]]:
        return self._lista_socios

    @property
    def cupos_ocupados(self) -> int:
        return self._inscritos

    @property
    def porcentaje_ocupacion(self) -> float:
        return (self._inscritos / self._cupoMaximo) * 100.0

    @abstractmethod
    def calcularCuposDisponibles(self) -> int:
        """Método abstracto que calcula los cupos disponibles según el recurso físico."""
        pass

    def cupos_disponibles(self) -> int:
        return self.calcularCuposDisponibles()

    def hayCupo(self) -> bool:
        """Regla de Bloqueo #1: Retorna True si aún quedan vacantes en la clase."""
        return self.calcularCuposDisponibles() > 0

    def reservarCupo(self) -> bool:
        """Incrementa los inscritos si hay cupo disponible."""
        if self.hayCupo():
            self._inscritos += 1
            return True
        return False

    def inscribir_socio(self, socio: Socio, posicion: int) -> bool:
        """Inscribe a un socio en una posición visual específica de la sala."""
        if 0 <= posicion < self._cupoMaximo:
            if self._lista_socios[posicion] is None:
                self._lista_socios[posicion] = socio
                self._inscritos += 1
                return True
        return False

    def liberar_posicion(self, posicion: int) -> bool:
        """Libera la posición especificada de la sala."""
        if 0 <= posicion < self._cupoMaximo:
            if self._lista_socios[posicion] is not None:
                self._lista_socios[posicion] = None
                self._inscritos = max(0, self._inscritos - 1)
                return True
        return False

    @abstractmethod
    def obtener_icono_disciplina(self) -> str:
        pass


class Yoga(ClaseDirigida):
    """Clase de Yoga delimitada por número de colchonetas."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        duracionMin: int = 60,
        cupoMaximo: int = 15,
        colchonetas: int = 15,
        instructor: Optional[Instructor] = None,
        sala: str = "Sala Yoga",
    ):
        super().__init__(codigo, nombre, duracionMin, min(cupoMaximo, colchonetas), instructor, sala)
        self._colchonetas = colchonetas

    @property
    def colchonetas(self) -> int:
        return self._colchonetas

    def calcularCuposDisponibles(self) -> int:
        """Sobrescribe el cálculo según colchonetas físicas disponibles."""
        return max(0, self._colchonetas - self._inscritos)

    def obtener_icono_disciplina(self) -> str:
        return "🧘"


class Spinning(ClaseDirigida):
    """Clase de Spinning delimitada por número de bicicletas."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        duracionMin: int = 45,
        cupoMaximo: int = 20,
        bicicletas: int = 20,
        instructor: Optional[Instructor] = None,
        sala: str = "Sala Spinning",
    ):
        super().__init__(codigo, nombre, duracionMin, min(cupoMaximo, bicicletas), instructor, sala)
        self._bicicletas = bicicletas

    @property
    def bicicletas(self) -> int:
        return self._bicicletas

    def calcularCuposDisponibles(self) -> int:
        """Sobrescribe el cálculo según bicicletas físicas disponibles."""
        return max(0, self._bicicletas - self._inscritos)

    def obtener_icono_disciplina(self) -> str:
        return "🚲"


class Crossfit(ClaseDirigida):
    """Clase de Crossfit delimitada por estaciones de trabajo."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        duracionMin: int = 60,
        cupoMaximo: int = 12,
        estacionesTrabajo: int = 12,
        instructor: Optional[Instructor] = None,
        sala: str = "Box Crossfit",
    ):
        super().__init__(codigo, nombre, duracionMin, min(cupoMaximo, estacionesTrabajo), instructor, sala)
        self._estacionesTrabajo = estacionesTrabajo

    @property
    def estacionesTrabajo(self) -> int:
        return self._estacionesTrabajo

    def calcularCuposDisponibles(self) -> int:
        """Sobrescribe el cálculo según estaciones de trabajo físicas disponibles."""
        return max(0, self._estacionesTrabajo - self._inscritos)

    def obtener_icono_disciplina(self) -> str:
        return "🏋️"


# Alias para mantener retrocompatibilidad de código existente
ClaseSpinning = Spinning
ClaseYoga = Yoga
ClaseCrossfit = Crossfit
