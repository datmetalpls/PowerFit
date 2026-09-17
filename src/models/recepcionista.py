"""Clase Recepcionista: Trabajador encargado de la atención, recepción y cobranza."""
from src.models.trabajador import Trabajador


class Recepcionista(Trabajador):
    """Especializa a un trabajador asignándole turno de atención y operaciones de recepción."""

    _turno: str

    def __init__(
        self,
        turno: str,
        idTrabajador: int,
        usuario: str,
        passHash: str,
        rut: str,
        nombres: str,
        apellidoPaterno: str,
        apellidoMaterno: str,
        telefono: str,
        correoElectronico: str,
    ):
        super().__init__(
            idTrabajador=idTrabajador,
            usuario=usuario,
            passHash=passHash,
            rol="Recepcionista",
            rut=rut,
            nombres=nombres,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
        )
        self._turno = turno

    def getTurno(self) -> str:
        """Retorna el turno de trabajo asignado (Mañana, Tarde, Noche)."""
        return self._turno

    def setTurno(self, nuevoTurno: str) -> None:
        """Modifica el turno de trabajo del recepcionista."""
        self._turno = nuevoTurno
