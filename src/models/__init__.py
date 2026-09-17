"""Modelos POO del sistema PowerFit."""
from .persona import Persona
from .direccion import Direccion
from .comuna import cargar_comunas_ine
from .trabajador import Trabajador
from .instructor import Instructor
from .recepcionista import Recepcionista
from .socio import Socio
from .administrador import Administrador

__all__ = [
    "Persona",
    "Direccion",
    "cargar_comunas_ine",
    "Trabajador",
    "Instructor",
    "Recepcionista",
    "Socio",
    "Administrador",
]
