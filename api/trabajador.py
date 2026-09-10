"""Clase base para trabajadores autenticados del gimnasio."""

from persona import Persona


class Trabajador(Persona):
    """Persona con credenciales y permisos operativos."""

    def __init__(
        self,
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
        # Función: asociar credenciales a una persona trabajadora.
        # Razón: el sistema debe distinguir usuarios internos y controlar acceso.
        super().__init__(
            rut,
            edad,
            nombres,
            apellidoPaterno,
            apellidoMaterno,
            telefono,
            correoElectronico,
            direccion,
        )
        self.idTrabajador = idTrabajador
        self.passHash = passHash
        self.permisos = set()

    def autenticar(self, passHash: str) -> bool:
        # Función: comparar la credencial recibida con el hash almacenado.
        # Razón: permite validar el acceso sin guardar la contraseña en texto plano.
        return self.passHash == passHash

    def cambiarPassword(self, nuevoHash: str) -> None:
        # Función: reemplazar el hash de la contraseña.
        # Razón: permite renovar credenciales comprometidas o vencidas.
        self.passHash = nuevoHash

    def tienePermiso(self, permiso: str) -> bool:
        # Función: consultar un permiso del trabajador.
        # Razón: deja un punto de extensión para autorización por rol.
        return permiso in self.permisos
