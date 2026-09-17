"""Clase Trabajador: Representa a los empleados autenticados del gimnasio PowerFit."""
from src.models.persona import Persona


class Trabajador(Persona):
    """Clase Trabajador heredada de Persona con credenciales y perfilamiento por rol (RBAC)."""

    def __init__(
        self,
        idTrabajador: int,
        usuario: str,
        passHash: str,
        rol: str,
        rut: str,
        nombres: str,
        apellidoPaterno: str,
        apellidoMaterno: str,
        telefono: str,
        correoElectronico: str,
    ):
        super().__init__(
            rut=rut,
            nombres=nombres,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
        )
        self._idTrabajador = idTrabajador
        self._usuario = usuario
        self._passHash = passHash
        self._rol = rol
        self._permisos = set()

    def getIdTrabajador(self) -> int:
        return self._idTrabajador

    def getUsuario(self) -> str:
        return self._usuario

    def getRol(self) -> str:
        return self._rol

    def setRol(self, nuevoRol: str) -> None:
        self._rol = nuevoRol

    def autenticar(self, password_intent: str) -> bool:
        """Valida si la contraseña ingresada coincide con la almacenada."""
        return self._passHash == password_intent

    def tienePermiso(self, permiso: str) -> bool:
        """Verifica si el trabajador posee un permiso específico."""
        if self._rol == "Administrador":
            return True
        return permiso in self._permisos

    def getDetallePerfil(self) -> str:
        """Implementa el método abstracto de Persona para Trabajadores."""
        return f"Trabajador: {self._nombres} {self._apellidoPaterno} | Rol: {self._rol} | RUT: {self._rut}"