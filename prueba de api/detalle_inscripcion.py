"""Detalle de una reserva o inscripción a una clase."""


class DetalleInscripcion:
    """Representa la reserva de un socio para un día de la semana."""

    def __init__(self, idDetalle: int, diaSemana: str):
        # Función: identificar la inscripción y su día reservado.
        # Razón: permite organizar los cupos y consultar reservas.
        self.idDetalle = idDetalle
        self.diaSemana = diaSemana
        self.reservada = False

    def reservar(self) -> bool:
        # Función: confirmar la reserva si aún no existe.
        # Razón: evita duplicar una misma inscripción.
        if self.reservada:
            return False
        self.reservada = True
        return True

    def cancelar(self) -> None:
        # Función: liberar la reserva actual.
        # Razón: devuelve el cupo cuando el socio desiste.
        self.reservada = False
