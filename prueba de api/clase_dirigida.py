"""Modelo base para las clases dirigidas del gimnasio."""


class ClaseDirigida:
    """Actividad con capacidad máxima y socios inscritos."""

    def __init__(self, codigo: int, nombre: str, cupoMaximo: int, duracionMinutos: int):
        # Función: definir la identidad, capacidad y duración de la actividad.
        # Razón: estos datos permiten planificar y controlar las sesiones.
        self.codigo = codigo
        self.nombre = nombre
        self.cupoMaximo = cupoMaximo
        self.duracionMinutos = duracionMinutos
        self.socios = []
        self.realizada = False

    def calcularCuposDisponibles(self) -> int:
        # Función: calcular capacidad restante.
        # Razón: informa si todavía se puede inscribir a otra persona.
        return max(0, self.cupoMaximo - len(self.socios))

    def capacidadExtraDisponible(self) -> int:
        # Función: indicar el límite adicional impuesto por el equipamiento.
        # Razón: las subclases pueden reducir la capacidad sin duplicar inscripciones.
        return self.calcularCuposDisponibles()

    def hayCupo(self) -> bool:
        # Función: indicar si queda al menos un cupo.
        # Razón: evita aceptar inscripciones cuando la clase está llena.
        return self.calcularCuposDisponibles() > 0

    def inscribirSocio(self, socio) -> bool:
        # Función: agregar un socio sin duplicarlo ni superar la capacidad.
        # Razón: protege la consistencia de las reservas de la clase.
        if self.capacidadExtraDisponible() <= 0 or socio in self.socios:
            return False
        self.socios.append(socio)
        return True

    def realizarClase(self) -> None:
        # Función: marcar la clase como realizada.
        # Razón: permite registrar que la sesión ocurrió.
        if not self.socios:
            raise ValueError("No se puede realizar una clase sin socios inscritos.")
        self.realizada = True
