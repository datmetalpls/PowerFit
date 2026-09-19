"""PowerFit - Transacciones de Inscripción Mensual (Requisito #4 UML Profesor)."""
from typing import List
from src.models.persona import Socio, ClaseDirigida


class DetalleInscripcion:
    """Representa el detalle individual de reserva para una clase dirigida en un día de la semana."""

    def __init__(self, diaSemana: str, clase: ClaseDirigida):
        self._diaSemana = diaSemana
        self._clase = clase
        self._confirmada = False

    @property
    def diaSemana(self) -> str:
        return self._diaSemana

    @property
    def clase(self) -> ClaseDirigida:
        return self._clase

    @property
    def confirmada(self) -> bool:
        return self._confirmada

    def confirmarReserva(self) -> bool:
        """Confirma la reserva si la clase asociada tiene cupo disponible."""
        if self._clase and self._clase.hayCupo():
            if self._clase.reservarCupo():
                self._confirmada = True
                return True
        return False


class InscripcionMensual:
    """Transacción compuesta por DetalleInscripcion (Composición 1 a 1..*)."""

    def __init__(self, mes: int, anio: int, socio: Socio):
        self._mes = mes
        self._anio = anio
        self._socio = socio
        self._detalles: List[DetalleInscripcion] = []

    @property
    def mes(self) -> int:
        return self._mes

    @property
    def anio(self) -> int:
        return self._anio

    @property
    def socio(self) -> Socio:
        return self._socio

    @property
    def detalles(self) -> List[DetalleInscripcion]:
        return self._detalles

    def agregarClase(self, clase: ClaseDirigida, diaSemana: str) -> bool:
        """Agrega una reserva a la inscripción mensual del socio."""
        if not self._socio.permitirIngreso():
            return False  # Bloqueo por membresía vencida

        detalle = DetalleInscripcion(diaSemana=diaSemana, clase=clase)
        if detalle.confirmarReserva():
            self._detalles.append(detalle)
            return True
        return False

    def cantidadReservas(self) -> int:
        """Retorna la cantidad total de reservas confirmadas en el mes."""
        return len(self._detalles)
