"""Modelos POO del sistema PowerFit."""
from .persona import Persona
from .direccion import Direccion
from .comuna import cargar_comunas_ine

__all__ = ["Persona", "Direccion", "cargar_comunas_ine"]
