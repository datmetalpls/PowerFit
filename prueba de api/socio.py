"""Modelo del socio del gimnasio."""

from datetime import date
from persona import Persona


class Socio(Persona):
    """Persona inscrita que puede mantener membresías y reservas."""

    def __init__(
        self,
        estadoActivo: bool,
        rut: str,
        edad: int,
        nombres: str,
        apellidoPaterno: str,
        apellidoMaterno: str,
        telefono: str,
        correoElectronico: str,
        direccion,
    ):
        # Función: asociar el estado de socio a los datos personales.
        # Razón: permite bloquear operaciones de socios inactivos.
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
        self.estadoActivo = estadoActivo
        self.membresias = []

    def crearFicha(self) -> None:
        # Función: preparar el registro de atención del socio.
        # Razón: centraliza la información necesaria para su seguimiento.
        if not hasattr(self, "ficha"):
            self.ficha = {
                "rut": self.getRut(),
                "nombre_completo": (
                    f"{self.getNombres()} {self.getApellidoPaterno()} "
                    f"{self.getApellidoMaterno()}"
                ),
                "contacto_emergencia": None,
                "observaciones": [],
            }

    def tieneMembresiaVigente(self, fecha: date | None = None) -> bool:
        # Función: revisar las membresías del socio para una fecha.
        # Razón: solo un socio vigente puede usar los servicios contratados.
        return self.estadoActivo and any(
            membresia.esVigente(fecha) for membresia in self.membresias
        )
