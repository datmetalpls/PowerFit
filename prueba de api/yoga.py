"""Clase dirigida especializada en yoga."""

from clase_dirigida import ClaseDirigida


class Yoga(ClaseDirigida):
    """Define el nivel de una clase de yoga."""

    def __init__(self, nivel: str, *args, **kwargs):
        # Función: agregar el nivel a la clase dirigida.
        # Razón: permite asignar sesiones adecuadas a cada participante.
        super().__init__(*args, **kwargs)
        self.nivel = nivel

    def calcularCuposDisponibles(self) -> int:
        # Función: reutilizar el cálculo común de cupos.
        # Razón: yoga comparte la regla de capacidad con otras clases.
        return super().calcularCuposDisponibles()

    def realizarClase(self) -> None:
        # Función: registrar que la sesión de yoga fue realizada.
        # Razón: deja una operación explícita para la agenda de clases.
        super().realizarClase()
