"""Powerfit - Modelos Backend POO para clases dirigidas y gestión de salas"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.models.socio import Socio

class ClaseDirigida(ABC):
    """Clase abstracta base para las clases dirigidas del gimnasio."""

    def __init__(
            self,
            codigo: str,
            nombre: str, 
            cupo_maximo: int,
            duracion_minutos: int = 60,
            sala: str= "Sala1",
    ):
            self._codigo = codigo
            self._nombre = nombre
            self._cupo_maximo= max(1, cupo_maximo)
            self._duracion_minutos = duracion_minutos
            self._sala = sala
            #Lista de cupos de la sala (none indica puesto Libre, o almacena un objeto Socio)
            self._cupos: List[Optional[Socio]] = [None] * self._cupo_maximo

    @property
    def codigo(self) -> str: 
         return self._codigo
    @property
    def nombre(self) -> str:
          return self._nombre
    @nombre.setter
    def nombre(self, valor: str):
          if not valor.strip():
                raise ValueError("El nombre de la clase no puede estar vacío.")
          self._nombre = valor.strip()
    @property
    def cupo_maximo(self) -> int:
          return self._cupo_maximo
    @property
    def duracion_minutos(self) -> int:
          return self._duracion_minutos
    @property
    def sala(self) -> str:
          return self._sala
    @property
    def cupos(self) -> List[Optional[Socio]]:
        return self._cupos
    @property
    def cupos_ocupados(self) -> int:
          return sum(1 for c in self._cupos if c is not None)
    @property
    def cupos_disponibles(self) -> int: 
          return self._cupo_maximo - self.cupos_ocupados
    @property
    def porcentaje_ocupacion(self) -> float:
          if self._cupo_maximo == 0:
                return 0.0
          return (self.cupos_ocupados/ self._cupo_maximo) * 100.0

    def inscribir_socio(self, socio: Socio, posicion: int) -> bool:
          """Inscribe a un socio en un puesto/bicicleta específico (0-indexed)."""
          if 0 <= posicion < self._cupo_maximo: 
                if self._cupos[posicion] is None:
                      self._cupos[posicion] = socio
                      return True
                return False

    def liberar_posicion(self, posicion: int) -> bool:
          """Libera la posición especificada si estaba ocupada."""
          if 0 <= posicion < self._cupo_maximo:
                self._cupos[posicion] = None
                return True
          return False

    @abstractmethod
    def obtener_icono_disciplina(self)-> str:
          """Retorna el emoji/icono que representa el puesto en la sala."""
          pass

class ClaseSpinning(ClaseDirigida):
          """Clase dirigida de Spinning con mapa de bicicletas."""

          def obtener_icono_disciplina(self) -> str:
                 return "🚲"

class ClaseYoga(ClaseDirigida):
          """Clase dirigida de Yoga con mapa de mats/colchonetas.""" 

          def obtener_icono_disciplina(self)->str:
                return "🧘"

class ClaseCrossfit(ClaseDirigida):
          """Clase dirigida de Crossfit con mapa de estaciones de entrenamiento."""

          def obtener_icono_disciplina(self)-> str: 
                return "🏋️"
          