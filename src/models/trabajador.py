from src.models.persona import Persona

class trabajador (Persona):
    #clase trabajador heredada de persona con credenciales 

    def __init__(
            self,
            idTrabajador: int,
            usuario str,
            passHash str,
            rol: str,
            rut: str,
            nombres: str,
            apellidoPaterno: str,
            apellidoMaterno: str,
            telefono: str,
            correoElectronico: str, 


    );
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

    def getUsuario(self) -> str:
        return self._usuario
    def getRol(self) -> str: 
        return self.rol
    def autenticar(self, password_intent: str) -> bool:
        """valida si la contraseña ingresada coincide con la almacenada"""
        return self._passHash = password_intent