"""Clase Administrador: Representa al usuario con máximo nivel de privilegios en PowerFit."""
from src.models.trabajador import Trabajador
from src.models.suplemento import Suplemento
from src.models.clase import ClaseDirigida


class Administrador(Trabajador):
    """Representa a un administrador heredando de Trabajador (UML posiblediagrama.drawio.xml)."""

    def __init__(
        self,
        nivelAcceso: str,
        idTrabajador: str,
        rut: str,
        nombres: str,
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
            rol="Administrador",
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
        )
        self._nivelAcceso = nivelAcceso

    @property
    def nivelAcceso(self) -> str:
        return self._nivelAcceso

    def getNivelAcceso(self) -> str:
        return self._nivelAcceso

    def setNivelAcceso(self, nuevoNivel: str) -> None:
        self._nivelAcceso = nuevoNivel

    def crearTrabajador(self, t: Trabajador) -> bool:
        """Crea o da de alta a un nuevo trabajador."""
        return True if t else False

    def crearClase(self, clase: ClaseDirigida) -> bool:
        """Registra una nueva clase dirigida."""
        return True if clase else False

    def modificarClase(self, clase: ClaseDirigida) -> bool:
        """Modifica parámetros de una clase dirigida."""
        return True if clase else False

    def reponerStock(self, sup: Suplemento, cant: int) -> None:
        """Repone stock de un suplemento."""
        if sup and cant > 0:
            sup.stock += cant