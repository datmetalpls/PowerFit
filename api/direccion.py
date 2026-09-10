# Clase Direccion: Representa la dirección física dentro del sistema PowerFit.
class Direccion:

    # Atributos de clase según la especificación del diagrama UML
    idDireccion: int
    tipoDireccion: str
    calle: str
    numero: str
    referencia: str

    # Valores permitidos para tipoDireccion
    TIPOS_DIRECCION = ["casa", "dpto","block"]

    # Método constructor que inicializa las instancias de la clase Direccion
    def __init__(
        self,
        idDireccion: int,
        tipoDireccion: str,
        calle: str,
        numero: str,
        referencia: str,
    ):
        self._idDireccion = idDireccion

        # Validación del tipo de dirección.
        # strip() elimina espacios al inicio y al final.
        # lower() convierte el texto a minúsculas.
        tipo_limpio = tipoDireccion.strip().lower()

        if tipo_limpio in self.TIPOS_DIRECCION:
            self._tipoDireccion = tipo_limpio
        else:
            raise ValueError(
                "El tipo de dirección solo puede ser 'casa' , 'dpto' o 'block'."
            )

        self._calle = calle
        self._numero = numero
        self._referencia = referencia

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

    # =========================================================================
    # MÉTODOS SETTER
    # =========================================================================

    def setTipoDireccion(self, tipoDireccion: str) -> None:
        """Modifica el tipo de dirección."""

        tipo_limpio = tipoDireccion.strip().lower()

        if tipo_limpio in self.TIPOS_DIRECCION:
            self._tipoDireccion = tipo_limpio
        else:
            raise ValueError(
                "El tipo de dirección solo puede ser 'casa' , 'dpto' o 'block'."
            )

    def setCalle(self, calle: str) -> None:
        """Modifica la calle de la dirección."""
        self._calle = calle

    def setNumero(self, numero: str) -> None:
        """Modifica el número de la dirección."""
        self._numero = numero

    def setReferencia(self, referencia: str) -> None:
        """Modifica la referencia de la dirección."""
        self._referencia = referencia
