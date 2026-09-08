# Clase Direccion: Representa la dirección física dentro del sistema PowerFit.
class Direccion:
    # Atributos de clase según la especificación del diagrama UML
    idDireccion: int
    tipoDireccion: str
    calle: str
    numero: str
    referencia: str

    # Método constructor que inicializa los atributos de la instancia Direccion
    def __init__(
        self,
        idDireccion: int,
        tipoDireccion: str,
        calle: str,
        numero: str,
        referencia: str,
    ):
        # Encapsulamiento de atributos con el prefijo '_' para indicar privacidad
        # Asignación del identificador único de la dirección
        self._idDireccion = idDireccion
        # Asignación del tipo de dirección
        self._tipoDireccion = tipoDireccion
        # Asignación del nombre de la calle
        self._calle = calle
        # Asignación del número de la dirección
        self._numero = numero
        # Asignación de la referencia de la dirección
        self._referencia = referencia

    # =========================================================================
    # MÉTODOS GETTER (Lectura de atributos)
    # =========================================================================

    # Obtiene y retorna el identificador de la dirección
    def getIdDireccion(self) -> int:
        """Retorna el id de la dirección."""
        return self._idDireccion

    # Obtiene y retorna el tipo de dirección
    def getTipoDireccion(self) -> str:
        """Retorna el tipo de dirección."""
        return self._tipoDireccion

    # Obtiene y retorna el nombre de la calle
    def getCalle(self) -> str:
        """Retorna la calle de la dirección."""
        return self._calle

    # Obtiene y retorna el número de la dirección
    def getNumero(self) -> str:
        """Retorna el número de la dirección."""
        return self._numero

    # Obtiene y retorna la referencia de la dirección
    def getReferencia(self) -> str:
        """Retorna la referencia de la dirección."""
        return self._referencia

    # =========================================================================
    # MÉTODOS SETTER (Modificación de atributos)
    # =========================================================================

    # Modifica y actualiza el identificador de la dirección
    def setIdDireccion(self, idDireccion: int) -> None:
        """Modifica el id de la dirección."""
        self._idDireccion = idDireccion

    # Modifica y actualiza el tipo de dirección
    def setTipoDireccion(self, tipoDireccion: str) -> None:
        """Modifica el tipo de dirección."""
        self._tipoDireccion = tipoDireccion

    # Modifica y actualiza el nombre de la calle
    def setCalle(self, calle: str) -> None:
        """Modifica la calle de la dirección."""
        self._calle = calle

    # Modifica y actualiza el número de la dirección
    def setNumero(self, numero: str) -> None:
        """Modifica el número de la dirección."""
        self._numero = numero

    # Modifica y actualiza la referencia de la dirección
    def setReferencia(self, referencia: str) -> None:
        """Modifica la referencia de la dirección."""
        self._referencia = referencia
