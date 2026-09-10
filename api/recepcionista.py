"""Trabajador que atiende operaciones de recepción."""

from trabajador import Trabajador


class Recepcionista(Trabajador):
    """Gestiona socios, cobros y ventas desde recepción."""

    def __init__(
        self,
        turno: str,
        idTrabajador: int,
        passHash: str,
        rut: str,
        edad: int,
        nombres: str,
        apellidoPaterno: str,
        apellidoMaterno: str,
        telefono: str,
        correoElectronico: str,
        direccion,
    ):
        # Función: registrar el turno de atención.
        # Razón: permite organizar la cobertura del servicio.
        super().__init__(
            idTrabajador,
            passHash,
            rut,
            edad,
            nombres,
            apellidoPaterno,
            apellidoMaterno,
            telefono,
            correoElectronico,
            direccion,
        )
        self.turno = turno

    def registrarSocio(self, socio) -> bool:
        # Función: activar un socio en recepción.
        # Razón: habilita sus operaciones dentro del gimnasio.
        socio.estadoActivo = True
        return True

    def cobrarMensualidad(self, socio) -> None:
        # Función: registrar que el socio fue atendido para su mensualidad.
        # Razón: deja un punto de integración con el sistema de pagos.
        if not socio.estadoActivo:
            raise ValueError("No se puede cobrar a un socio inactivo.")
        if not socio.membresias:
            raise ValueError("El socio no tiene una membresía para renovar.")
        socio.membresias[-1].renovar()
        socio.mensualidadCobrada = True

    def registrarVenta(self, venta) -> bool:
        # Función: aceptar una venta ya construida.
        # Razón: centraliza el registro de operaciones comerciales.
        if venta is None or not venta.detalles:
            return False
        if any(not detalle.confirmarStock() for detalle in venta.detalles):
            return False
        return venta.calcularTotal() > 0
