"""Paquete de modelos del dominio POO para PowerFit Gym System (UML posiblediagrama.drawio.xml)."""

from src.models.persona import Persona
from src.models.socio import Socio
from src.models.trabajador import Trabajador
from src.models.instructor import Instructor
from src.models.recepcionista import Recepcionista
from src.models.administrador import Administrador
from src.models.clase import (
    Clase,
    ClaseDirigida,
    Yoga,
    Spinning,
    Crossfit,
    ClaseYoga,
    ClaseSpinning,
    ClaseCrossfit,
)
from src.models.direccion import Direccion
from src.models.comuna import Comuna, cargar_comunas_ine
from src.models.inscripcion import InscripcionMensual, DetalleInscripcion
from src.models.suplemento import (
    Suplemento,
    IndicadorDolar,
    Venta,
    DetalleVenta,
)

__all__ = [
    "Persona",
    "Socio",
    "Trabajador",
    "Instructor",
    "Recepcionista",
    "Administrador",
    "Clase",
    "ClaseDirigida",
    "Yoga",
    "Spinning",
    "Crossfit",
    "ClaseYoga",
    "ClaseSpinning",
    "ClaseCrossfit",
    "Direccion",
    "Comuna",
    "cargar_comunas_ine",
    "InscripcionMensual",
    "DetalleInscripcion",
    "Suplemento",
    "IndicadorDolar",
    "Venta",
    "DetalleVenta",
]
