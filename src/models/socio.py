"""Clase Socio: Representa a los clientes afiliados del gimnasio PowerFit."""
from datetime import date, timedelta
from typing import Optional
from src.models.persona import Persona
from src.models.excepciones import MembresiaVencidaException


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
        fechaIngreso: str = "",
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
        self._fechaIngreso = fechaIngreso

    @property
    def idSocio(self) -> int:
        return self._idSocio

    @idSocio.setter
    def idSocio(self, nuevo_id: int):
        self._idSocio = int(nuevo_id)

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
        if not self._estadoActivo:
            raise MembresiaVencidaException("El socio tiene su plan cancelado/desactivado.")
        if self._fechaVencimientoMembresia is None or self._fechaVencimientoMembresia < date.today():
            raise MembresiaVencidaException("La membresía del socio se encuentra vencida.")
        return True

    def renovarMembresia(self, dias: int = 30) -> None:
        """UML: + renovarMembresia(dias: int): void - Extiende la membresía y activa el estado."""
        base_fecha = max(date.today(), self._fechaVencimientoMembresia)
        self._fechaVencimientoMembresia = base_fecha + timedelta(days=dias)
        self._estadoActivo = True

    def cancelarPlan(self) -> None:
        """Marca la cuenta/plan como cancelado/desactivado."""
        self._estadoActivo = False

    def cancelarMembresia(self) -> None:
        """UML: Cancela y desactiva la membresía del socio."""
        self.cancelarPlan()

    @property
    def estado_membresia(self) -> str:
        """Determina el estado actual de la membresía ('Inactivo', 'Al Día' o 'Vencida')."""
        if not self._estadoActivo:
            return "Inactivo"
        if self._fechaVencimientoMembresia and self._fechaVencimientoMembresia >= date.today():
            return "Al Día"
        return "Vencida"

    @property
    def esta_al_dia(self) -> bool:
        """Indica si el socio se encuentra al día y con membresía vigente."""
        return self.estado_membresia == "Al Día"

    @classmethod
    def crear_con_estado(
        cls,
        idSocio: int,
        rut: str,
        nombres: str,
        apellidoPaterno: str = "",
        apellidoMaterno: str = "",
        telefono: str = "",
        correoElectronico: str = "",
        tipo_estado: str = "Al Día",
    ) -> "Socio":
        """Método de fábrica que construye un Socio calculando vigencia según el estado inicial."""
        if "Al Día" in tipo_estado:
            fecha_venc = date.today() + timedelta(days=30)
            activo = True
        elif "Vencida" in tipo_estado:
            fecha_venc = date.today() - timedelta(days=1)
            activo = True
        else:
            fecha_venc = date.today()
            activo = False

        return cls(
            idSocio=idSocio,
            rut=rut,
            nombres=nombres,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
            fechaVencimientoMembresia=fecha_venc,
            estadoActivo=activo,
        )

    @property
    def fechaIngreso(self) -> str:
        return self._fechaIngreso
