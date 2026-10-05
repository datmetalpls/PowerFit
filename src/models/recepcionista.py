"""Clase Recepcionista: Trabajador encargado de la atención, recepción y cobranza."""
from datetime import date
from typing import Optional
from src.models.trabajador import Trabajador
from src.models.socio import Socio
from src.models.suplemento import Venta


class Recepcionista(Trabajador):
    """Recepcionista encargada de inscripciones, pagos, cobranza y alta de socios (UML posiblediagrama.drawio.xml)."""

    def __init__(
        self,
        idTrabajador: str,
        rut: str,
        nombres: str,
        turno: str = "Mañana",
        usuario: str = "",
        passHash: str = "",
        apellidoPaterno: str = "",
        apellidoMaterno: str = "",
        telefono: str = "",
        correoElectronico: str = "",
        **kwargs,
    ):
        super().__init__(
            idTrabajador=idTrabajador,
            rut=rut,
            nombres=nombres,
            usuario=usuario,
            passHash=passHash,
            rol="Recepcionista",
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
        )
        self._turno = turno
        self._socios_registrados = []
        self._ventas_procesadas = []

    @property
    def turno(self) -> str:
        return self._turno

    def getTurno(self) -> str:
        return self._turno

    def registrarSocio(self, socio: Socio) -> bool:
        """Registra a un nuevo socio en el sistema (UML: + registrarSocio(socio: Socio): boolean)."""
        if socio and socio not in self._socios_registrados:
            self._socios_registrados.append(socio)
            return True
        return False

    def cobrarMensualidad(self, socio: Socio, monto: float) -> None:
        """Cobrar mensualidad al socio (UML: + cobrarMensualidad(socio: Socio, monto: double): void)."""
        if socio and monto > 0:
            from datetime import timedelta
            socio.fechaVencimientoMembresia = date.today() + timedelta(days=30)

    def crearInscripcion(self, s: Socio, mes: int, anio: int):
        """Crea una InscripcionMensual (UML: + crearInscripcion(s: Socio, mes: int, anio: int): InscripcionMensual)."""
        from src.models.inscripcion import InscripcionMensual
        return InscripcionMensual(mes=mes, anio=anio, socio=s)

    def registrarVenta(self, venta: Venta) -> bool:
        """Registra una venta procesada (UML: + registrarVenta(venta: Venta): boolean)."""
        if venta:
            self._ventas_procesadas.append(venta)
            return True
        return False
