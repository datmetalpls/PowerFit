"""Clase Socio: Representa a los clientes afiliados del gimnasio PowerFit."""
from src.models.persona import Persona


class Socio(Persona):
    """Representa a un cliente socio heredando atributos personales de Persona."""

    _idSocio: int
    _estadoActivo: bool
    _direccion: object

    def __init__(
        self,
        idSocio: int,
        rut: str,
        nombres: str,
        apellidoPaterno: str,
        apellidoMaterno: str,
        telefono: str,
        correoElectronico: str,
        direccion=None,
        estadoActivo: bool = True,
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
        self._direccion = direccion
        self._estadoActivo = estadoActivo

    def getIdSocio(self) -> int:
        """Retorna el ID único del socio."""
        return self._idSocio

    def getDireccion(self):
        """Retorna el objeto Direccion asociado al socio."""
        return self._direccion

    def setDireccion(self, nuevaDireccion) -> None:
        """Asigna o actualiza la dirección del socio."""
        self._direccion = nuevaDireccion

    def isEstadoActivo(self) -> bool:
        """Retorna el estado de la membresía del socio (True: Activo, False: Inactivo)."""
        return self._estadoActivo

    def setEstadoActivo(self, estado: bool) -> None:
        """Modifica el estado de actividad del socio."""
        self._estadoActivo = estado
