"""Clase Direccion: Representa la dirección física y postal dentro del sistema PowerFit."""
from typing import Optional
from src.models.comuna import Comuna


class Direccion:
    """Representa la ubicación física de un individuo o entidad en PowerFit."""

    # Valores permitidos para tipoDireccion
    TIPOS_DIRECCION = ["casa", "dpto", "block"]

    def __init__(
        self,
        idDireccion: int,
        tipoDireccion: str,
        calle: str,
        numero: str,
        referencia: str = "",
        comuna: Optional[Comuna] = None,
    ):
        self._idDireccion = idDireccion

        tipo_limpio = tipoDireccion.strip().lower()
        if tipo_limpio in self.TIPOS_DIRECCION:
            self._tipoDireccion = tipo_limpio
        else:
            raise ValueError(
                "El tipo de dirección solo puede ser 'casa', 'dpto' o 'block'."
            )

        self._calle = calle
        self._numero = numero
        self._referencia = referencia
        self._comuna = comuna

    # =========================================================================
    # MÉTODOS GETTER
    # =========================================================================

    def getIdDireccion(self) -> int:
        """Retorna el id de la dirección."""
        return self._idDireccion

    def getTipoDireccion(self) -> str:
        """Retorna el tipo de dirección."""
        return self._tipoDireccion

    def getCalle(self) -> str:
        """Retorna la calle de la dirección."""
        return self._calle

    def getNumero(self) -> str:
        """Retorna el número de la dirección."""
        return self._numero

    def getReferencia(self) -> str:
        """Retorna la referencia de la dirección."""
        return self._referencia

    def getComuna(self) -> Optional[Comuna]:
        """Retorna el objeto Comuna asociado."""
        return self._comuna

    # =========================================================================
    # MÉTODOS SETTER
    # =========================================================================

    def setIdDireccion(self, idDireccion: int) -> None:
        self._idDireccion = idDireccion

    def setTipoDireccion(self, tipoDireccion: str) -> None:
        tipo_limpio = tipoDireccion.strip().lower()
        if tipo_limpio in self.TIPOS_DIRECCION:
            self._tipoDireccion = tipo_limpio
        else:
            raise ValueError(
                "El tipo de dirección solo puede ser 'casa', 'dpto' o 'block'."
            )

    def setCalle(self, calle: str) -> None:
        self._calle = calle

    def setNumero(self, numero: str) -> None:
        self._numero = numero

    def setReferencia(self, referencia: str) -> None:
        self._referencia = referencia

    def setComuna(self, comuna: Optional[Comuna]) -> None:
        """Asocia la Comuna correspondiente."""
        self._comuna = comuna

    # =========================================================================
    # MÉTODO HELPER DE FORMATEO COMPLETO
    # =========================================================================

    def obtenerDireccionCompleta(self) -> str:
        """Retorna el texto formateado de la dirección completa con su Comuna."""
        ref_text = f" ({self._referencia})" if self._referencia else ""
        comuna_text = f", {self._comuna.nombre}" if self._comuna else ""
        return f"{self._tipoDireccion.capitalize()} {self._calle} #{self._numero}{ref_text}{comuna_text}"