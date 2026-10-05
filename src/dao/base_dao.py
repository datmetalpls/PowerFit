# DAO Base / Interfaz genérica o conexión

from abc import ABC, abstractmethod
from typing import List, Any, Optional

class BaseDAO(ABC):
    """Inteerfaz base abstracta para los DAO de powerfit"""

    @abstractmethod
    def obtener_todos(self)-> List[Any]:
        """Obtiene todas las entidades registradas"""
        pass

    @abstractmethod
    def obtener_por_id(self, id_entidad: int)-> Optional[Any]:
        """Busca una entidad por su ID primaria"""
        pass

    @abstractmethod
    def guardar(self, entidad: Any) -> bool:
        """Inserta o actualiza una entidad en la base de datos"""
        pass

    @abstractmethod
    def eliminar(self, id_entidad: int) -> bool: 
        """ELimina una entidad por su ID primario."""
        pass

