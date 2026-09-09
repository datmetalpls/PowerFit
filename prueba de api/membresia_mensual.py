"""Modelo de la vigencia mensual de un socio."""

from calendar import monthrange
from datetime import date


class MembresiaMensual:
    """Registra el período contratado y su estado de vigencia."""

    def __init__(self, fechaInicio: date, fechaTermino: date, vigente: bool = True):
        # Función: guardar las fechas y estado de la membresía.
        # Razón: permite controlar el acceso según el período pagado.
        self.fechaInicio = fechaInicio
        self.fechaTermino = fechaTermino
        self.vigente = vigente

    def renovar(self, meses: int = 1) -> None:
        # Función: extender el término de la membresía.
        # Razón: permite continuar el servicio sin crear un registro innecesario.
        if meses <= 0:
            raise ValueError("La cantidad de meses debe ser mayor que cero.")
        totalMeses = self.fechaTermino.month - 1 + meses
        nuevoAnio = self.fechaTermino.year + totalMeses // 12
        nuevoMes = totalMeses % 12 + 1
        nuevoDia = min(
            self.fechaTermino.day,
            monthrange(nuevoAnio, nuevoMes)[1],
        )
        self.fechaTermino = date(nuevoAnio, nuevoMes, nuevoDia)
        self.vigente = True

    def esVigente(self, fecha: date | None = None) -> bool:
        # Función: comprobar si la fecha está dentro del período contratado.
        # Razón: protege el acceso de personas con membresías vencidas.
        fechaConsulta = fecha or date.today()
        return self.vigente and self.fechaInicio <= fechaConsulta <= self.fechaTermino
