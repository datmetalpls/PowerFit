"""Clase Trabajador: Representa a los empleados autenticados del gimnasio PowerFit."""
from abc import ABC
from src.models.persona import Persona


class Trabajador(Persona, ABC):
    """Clase abstracta base para empleados con perfilamiento por ID y permisos."""

    def __init__(
        self,
        idTrabajador: str,
        rut: str,
        nombres: str,
        usuario: str = "",
        passHash: str = "",
        rol: str = "Trabajador",
        apellidoPaterno: str = "",
        apellidoMaterno: str = "",
        telefono: str = "",
        correoElectronico: str = "",
        **kwargs,
    ):
        super().__init__(
            rut=rut,
            nombres=nombres,
            apellidoPaterno=apellidoPaterno,
            apellidoMaterno=apellidoMaterno,
            telefono=telefono,
            correoElectronico=correoElectronico,
        )
        self._idTrabajador = str(idTrabajador)
        self._usuario = usuario or nombres.lower().replace(" ", "")
        self._passHash = passHash
        self._rol = rol
        self._permisos = set()

    @property
    def idTrabajador(self) -> str:
        return self._idTrabajador

    @property
    def usuario(self) -> str:
        return self._usuario

    @property
    def rol(self) -> str:
        return self._rol

    def getRol(self) -> str:
        return self._rol

    def autenticar(self, password_intent: str) -> bool:
        return self._passHash == password_intent

    def tienePermiso(self, accion: str) -> bool:
        """Verifica si el trabajador posee permiso para ejecutar una acción."""
        if self._rol == "Administrador":
            return True
        return accion in self._permisos