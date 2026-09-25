"""Clase Instructor: Trabajador especialista encargado de impartir disciplinas deportivas."""
from src.models.trabajador import Trabajador
from src.models.socio import Socio


class Instructor(Trabajador):
    """Instructor que dicta clases dirigidas y registra asistencia."""

    def __init__(
        self,
        especialidad: str,
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
            rol="Instructor",
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
        )
        self._especialidad = especialidad
        self._clases_dictadas = []

    @property
    def especialidad(self) -> str:
        return self._especialidad

    def getEspecialidad(self) -> str:
        return self._especialidad

    def dictarClase(self, clase) -> None:
        """Asigna la clase para dictarla."""
        if clase not in self._clases_dictadas:
            self._clases_dictadas.append(clase)

    def marcarAsistencia(self, socio: Socio, clase) -> bool:
        """Registra la presencia del socio en la clase."""
        if socio.permitirIngreso() and clase.hayCupo():
            return clase.reservarCupo()
        return False
