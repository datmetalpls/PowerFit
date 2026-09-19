"""Paquete de modelos del dominio POO para PowerFit Gym System (UML Oficial)."""

from src.models.persona import (
    Persona,
    Socio,
    Trabajador,
    Instructor,
    Recepcionista,
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
from src.models.suplemento import Suplemento, IndicadorDolar

__all__ = [
    "Persona",
    "Socio",
    "Trabajador",
    "Instructor",
    "Recepcionista",
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
]
