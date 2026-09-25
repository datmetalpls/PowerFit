"""Clase Socio: Representa a los clientes afiliados del gimnasio PowerFit."""
from datetime import date, timedelta
from typing import Optional
from src.models.persona import Persona


class Socio(Persona):
    """Representa a un Socio con fecha de vencimiento y control de ingreso (UML posiblediagrama.drawio.xml)."""

    def __init__(
        self,
        idSocio: int,
        rut: str,
        nombres: str,
        apellidoPaterno: str = "",
        fechaVencimientoMembresia: Optional[date] = None,
        estadoActivo: bool = True,
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
        self._estadoActivo = estadoActivo

    @property
    def idSocio(self) -> int:
        return self._idSocio

    @property
    def fechaVencimientoMembresia(self) -> date:
        return self._fechaVencimientoMembresia

    @fechaVencimientoMembresia.setter
    def fechaVencimientoMembresia(self, nueva_fecha: date):
        self._fechaVencimientoMembresia = nueva_fecha

    @property
    def estadoActivo(self) -> bool:
        return self._estadoActivo

    @estadoActivo.setter
    def estadoActivo(self, estado: bool):
        self._estadoActivo = estado

    def getIdSocio(self) -> int:
        return self._idSocio

    def permitirIngreso(self) -> bool:
        """Regla de Bloqueo UML: Retorna True solo si está activo y la membresía no ha vencido."""
        if not self._estadoActivo or self._fechaVencimientoMembresia is None:
            return False
        return self._fechaVencimientoMembresia >= date.today()

    def renovarMembresia(self, dias: int = 30) -> None:
        """UML: + renovarMembresia(dias: int): void - Extiende la membresía y activa el estado."""
        base_fecha = max(date.today(), self._fechaVencimientoMembresia)
        self._fechaVencimientoMembresia = base_fecha + timedelta(days=dias)
        self._estadoActivo = True

    def cancelarPlan(self) -> None:
        """Marca la cuenta/plan como cancelado/desactivado."""
        self._estadoActivo = False
