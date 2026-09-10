"""Clase dirigida especializada en spinning."""

from clase_dirigida import ClaseDirigida


class Spinning(ClaseDirigida):
    """Controla las bicicletas disponibles para una sesión de spinning."""

    def __init__(
        self,
        bicicletasDisponibles: int,
        codigo: int,
        nombre: str,
        cupoMaximo: int,
        duracionMinutos: int,
    ):
        # Función: registrar el equipamiento disponible de la clase.
        # Razón: la capacidad real depende de las bicicletas utilizables.
        super().__init__(codigo, nombre, cupoMaximo, duracionMinutos)
        self.bicicletasDisponibles = bicicletasDisponibles

    def calcularCuposDisponibles(self) -> int:
        # Función: limitar los cupos por bicicletas y capacidad general.
        # Razón: no se deben aceptar más alumnos que equipos disponibles.
        return max(0, min(self.cupoMaximo, self.bicicletasDisponibles) - len(self.socios))

    def capacidadExtraDisponible(self) -> int:
        return self.calcularCuposDisponibles()

    def realizarClase(self) -> None:
        # Función: marcar la sesión como realizada.
        # Razón: permite registrar el cumplimiento de la actividad.
        super().realizarClase()
