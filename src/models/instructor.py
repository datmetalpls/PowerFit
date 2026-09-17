"""Clase Instructor: Trabajador especialista encargado de impartir disciplinas deportivas."""
from src.models.trabajador import Trabajador


class Instructor(Trabajador):
    """Especializa a un trabajador asignándole una disciplina profesional."""

    _especialidad: str

    def __init__(
        self,
        especialidad: str,
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
            rol="Instructor",
            rut=rut,
            nombres=nombres,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
        )
        self._especialidad = especialidad
        self._clasesAsignadas = []

    def getEspecialidad(self) -> str:
        """Retorna la disciplina en la que se especializa el instructor."""
        return self._especialidad

    def setEspecialidad(self, nuevaEspecialidad: str) -> None:
        """Modifica la especialidad del instructor."""
        self._especialidad = nuevaEspecialidad

    def getClasesAsignadas(self) -> list:
        """Retorna el listado de clases dirigidas asignadas al instructor."""
        return self._clasesAsignadas

    def asignarClase(self, clase) -> None:
        """Asocia una clase al historial del instructor."""
        if clase not in self._clasesAsignadas:
            self._clasesAsignadas.append(clase)
