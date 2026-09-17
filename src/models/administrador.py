"""Clase Administrador: Representa al usuario con máximo nivel de privilegios en PowerFit."""
from src.models.trabajador import Trabajador

class Administrador(Trabajador):

    #Representa a un admin heredando de trabajador

    def __init__(
            self,
            nivelAcceso: str,
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
                  rol="Administrador",
                  rut=rut,
                  nombres=nombres,
                  apellidoPaterno=apellidoPaterno,
                  apellidoMaterno=apellidoMaterno,
                  telefono=telefono,
                  correoElectronico=correoElectronico,
            )
        self._nivelAcceso = nivelAcceso
    def getNivelAcceso(self) -> str:
          #retorna nivel de acceso del admin
          return self._nivelAcceso
    def setNivelAcceso(self, nuevoNivel: str) -> None:
          #modifica el nivel de acceso del admin
          self._nivelAcceso = nuevoNivel