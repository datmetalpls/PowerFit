"""Clase ClaseDirigida: Modelos POO de clases dirigidas y disciplinas."""
from src.models.persona import (
    ClaseDirigida as ClaseDirigidaOficial,
    Yoga,
    Spinning,
    Crossfit,
)


class ClaseDirigida(ClaseDirigidaOficial):
    pass


ClaseSpinning = Spinning
ClaseYoga = Yoga
ClaseCrossfit = Crossfit