"""PowerFit - Jerarquía de Clases y Disciplinas (UML posiblediagrama.drawio.xml)."""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.socio import Socio
from src.models.instructor import Instructor


class Clase(ABC):
    """Clase abstracta base Clase según el diagrama UML posiblediagrama.drawio.xml."""

    def __init__(self, codigo: str, nombre: str, duracionMin: int):
        self._codigo = codigo
        self._nombre = nombre
        self._duracionMin = duracionMin

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


class ClaseDirigida(Clase, ABC):
    """Clase abstracta ClaseDirigida que hereda de Clase."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        duracionMin: int,
        cupoMaximo: int,
        instructor: Optional[Instructor] = None,
        sala: str = "Sala 1",
    ):
        super().__init__(codigo=codigo, nombre=nombre, duracionMin=duracionMin)
        self._cupoMaximo = max(1, cupoMaximo)
        self._inscritos = 0
        self._instructor = instructor
        self._sala = sala
        self._lista_socios: List[Optional[Socio]] = [None] * self._cupoMaximo

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
        instructor: Optional[Instructor] = None,
        sala: str = "Sala Yoga",
        colchonetas: Optional[int] = None,
    ):
        colch = colchonetas if colchonetas is not None else cupoMaximo
        super().__init__(
            codigo=codigo,
            nombre=nombre,
            duracionMin=duracionMin,
            cupoMaximo=min(cupoMaximo, colch),
            instructor=instructor,
            sala=sala,
        )
        self._colchonetas = colch

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
        instructor: Optional[Instructor] = None,
        sala: str = "Sala Spinning",
        bicicletas: Optional[int] = None,
    ):
        bici = bicicletas if bicicletas is not None else cupoMaximo
        super().__init__(
            codigo=codigo,
            nombre=nombre,
            duracionMin=duracionMin,
            cupoMaximo=min(cupoMaximo, bici),
            instructor=instructor,
            sala=sala,
        )
        self._bicicletas = bici

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
        instructor: Optional[Instructor] = None,
        sala: str = "Box Crossfit",
        estacionesTrabajo: Optional[int] = None,
    ):
        est = estacionesTrabajo if estacionesTrabajo is not None else cupoMaximo
        super().__init__(
            codigo=codigo,
            nombre=nombre,
            duracionMin=duracionMin,
            cupoMaximo=min(cupoMaximo, est),
            instructor=instructor,
            sala=sala,
        )
        self._estacionesTrabajo = est

    @property
    def estacionesTrabajo(self) -> int:
        return self._estacionesTrabajo

    def calcularCuposDisponibles(self) -> int:
        """Sobrescribe el cálculo según estaciones de trabajo físicas disponibles."""
        return max(0, self._estacionesTrabajo - self._inscritos)

    def obtener_icono_disciplina(self) -> str:
        return "🏋️"


# Alias para mantener retrocompatibilidad
ClaseSpinning = Spinning
ClaseYoga = Yoga
ClaseCrossfit = Crossfit