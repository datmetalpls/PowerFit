"""Clase dirigida especializada en crossfit."""

from clase_dirigida import ClaseDirigida


class Crossfit(ClaseDirigida):
    """Controla las estaciones disponibles para una sesión de crossfit."""

    def __init__(
        self,
        estacionesDisponibles: int,
        codigo: int,
        nombre: str,
        cupoMaximo: int,
        duracionMinutos: int,
    ):
        # Función: registrar el equipamiento disponible para la clase.
        # Razón: la capacidad está limitada por las estaciones de trabajo.
        super().__init__(codigo, nombre, cupoMaximo, duracionMinutos)
        self.estacionesDisponibles = estacionesDisponibles

    def calcularCuposDisponibles(self) -> int:
        # Función: calcular cupos considerando capacidad y estaciones.
        # Razón: evita sobrecargar el espacio de entrenamiento.
        return max(0, min(self.cupoMaximo, self.estacionesDisponibles) - len(self.socios))

    def capacidadExtraDisponible(self) -> int:
        return self.calcularCuposDisponibles()

    def realizarClase(self) -> None:
        # Función: marcar la sesión como realizada.
        # Razón: conserva el estado de ejecución de la actividad.
        super().realizarClase()
