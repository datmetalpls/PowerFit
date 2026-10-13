"""Clase Trabajador: Representa a los empleados autenticados del gimnasio PowerFit."""
from abc import ABC
from src.models.persona import Persona
from src.utils.security import GestorSeguridad


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
        if passHash and not GestorSeguridad.es_hash_argon2(passHash):
            self._passHash = GestorSeguridad.hashear_password(passHash)
        else:
            self._passHash = passHash or ""
        self._cuenta_bloqueada = False
        self._intentos_fallidos = 0
        self._rol = rol
        self._permisos = set()

    @property
    def idTrabajador(self) -> str:
        return self._idTrabajador

    @property
    def cuenta_bloqueada(self) -> bool:
        return self._cuenta_bloqueada

    @property
    def intentos_fallidos(self) -> int:
        return self._intentos_fallidos

    def registrar_intento_fallido(self) -> int:
        """Registra un fallo de login y bloquea la cuenta al alcanzar 3 intentos."""
        self._intentos_fallidos += 1
        if self._intentos_fallidos >= 3:
            self.bloquear()
        return self._intentos_fallidos

    def reiniciar_intentos(self):
        """Restablece el contador de intentos fallidos."""
        self._intentos_fallidos = 0

    def bloquear(self):
        self._cuenta_bloqueada = True

    def desbloquear(self):
        self._cuenta_bloqueada = False
        self._intentos_fallidos = 0

    @property
    def usuario(self) -> str:
        return self._usuario

    @property
    def rol(self) -> str:
        return self._rol

    def getRol(self) -> str:
        return self._rol

    @property
    def passHash(self) -> str:
        return self._passHash

    @passHash.setter
    def passHash(self, nueva_clave: str):
        if not nueva_clave:
            self._passHash = ""
        elif GestorSeguridad.es_hash_argon2(nueva_clave):
            self._passHash = nueva_clave
        else:
            self._passHash = GestorSeguridad.hashear_password(nueva_clave)

    def cambiar_password(self, nueva_clave: str):
        """Actualiza la contraseña del trabajador almacenando su hash Argon2id."""
        self.passHash = nueva_clave

    def autenticar(self, password_intent: str) -> bool:
        """Valida las credenciales contra el hash Argon2id; si falla, computa el intento y bloquea a los 3 fallos."""
        if self._cuenta_bloqueada:
            return False
        if GestorSeguridad.verificar_password(self._passHash, password_intent):
            self.reiniciar_intentos()
            return True
        self.registrar_intento_fallido()
        return False

    def tienePermiso(self, accion: str) -> bool:
        """Verifica si el trabajador posee permiso para ejecutar una acción."""
        if self._rol == "Administrador":
            return True
        return accion.lower() in self._permisos

    @classmethod
    def crear(
        cls,
        rol: str,
        idTrabajador: str,
        rut: str,
        nombres: str,
        apellidoPaterno: str = "",
        apellidoMaterno: str = "",
        usuario: str = "",
        passHash: str = "",
        **kwargs,
    ) -> "Trabajador":
        """Método de Fábrica (Factory Method) para instanciar subclases polimórficas de Trabajador."""
        from src.models.administrador import Administrador
        from src.models.recepcionista import Recepcionista
        from src.models.instructor import Instructor

        if rol == "Recepcionista":
            return Recepcionista(
                idTrabajador=idTrabajador,
                rut=rut,
                nombres=nombres,
                apellidoPaterno=apellidoPaterno,
                apellidoMaterno=apellidoMaterno,
                usuario=usuario,
                passHash=passHash,
                **kwargs,
            )
        elif rol == "Instructor":
            return Instructor(
                especialidad=kwargs.get("especialidad", "Fitness"),
                idTrabajador=idTrabajador,
                rut=rut,
                nombres=nombres,
                apellidoPaterno=apellidoPaterno,
                apellidoMaterno=apellidoMaterno,
                usuario=usuario,
                passHash=passHash,
            )
        else:
            return Administrador(
                nivelAcceso=kwargs.get("nivelAcceso", "General"),
                idTrabajador=idTrabajador,
                rut=rut,
                nombres=nombres,
                apellidoPaterno=apellidoPaterno,
                apellidoMaterno=apellidoMaterno,
                usuario=usuario,
                passHash=passHash,
            )