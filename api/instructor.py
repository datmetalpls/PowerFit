"""Trabajador encargado de impartir clases."""

from trabajador import Trabajador


class Instructor(Trabajador):
    """Especializa a un trabajador con una disciplina profesional."""

    def __init__(
        self,
        especialidad: str,
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
        # Función: registrar la especialidad del instructor.
        # Razón: permite asignarlo a clases acordes a su formación.
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
        self.especialidad = especialidad

    def dictarClase(self, clase) -> None:
        # Función: asociar al instructor como responsable de una clase.
        # Razón: deja trazabilidad de quién dirige la actividad.
        clase.instructor = self

    def marcarAsistencia(self, socio, clase) -> None:
        # Función: registrar la asistencia de un socio.
        # Razón: permite controlar participación y seguimiento.
        if not hasattr(self, "asistencias"):
            self.asistencias = []
        if not hasattr(clase, "asistencias"):
            clase.asistencias = []
        if socio not in clase.asistencias:
            clase.asistencias.append(socio)
        if (clase, socio) not in self.asistencias:
            self.asistencias.append((clase, socio))
