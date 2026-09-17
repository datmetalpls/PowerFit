"""Clase Base Abstracta Persona: Representa la entidad fundamental de personas en PowerFit."""
from abc import ABC, abstractmethod
import re


class Persona(ABC):
    """Clase base abstracta que define la interfaz e identidad de todas las personas del sistema."""

    _rut: str
    _nombres: str
    _apellidoPaterno: str
    _apellidoMaterno: str
    _telefono: str
    _correoElectronico: str

    def __init__(
        self,
        rut: str,
        nombres: str,
        apellidoPaterno: str,
        apellidoMaterno: str,
        telefono: str,
        correoElectronico: str,
    ):
        self._rut = rut
        self._nombres = nombres
        self._apellidoPaterno = apellidoPaterno
        self._apellidoMaterno = apellidoMaterno
        self._telefono = telefono
        self._correoElectronico = correoElectronico

    # =========================================================================
    # DECORADORES @PROPERTY (Encapsulamiento Pythonico)
    # =========================================================================

    @property
    def rut(self) -> str:
        """Propiedad para acceder al RUT inmutable."""
        return self._rut

    @property
    def nombres(self) -> str:
        """Propiedad para acceder a los nombres inmutables."""
        return self._nombres

    @property
    def apellidoPaterno(self) -> str:
        """Propiedad para acceder al apellido paterno inmutable."""
        return self._apellidoPaterno

    @property
    def apellidoMaterno(self) -> str:
        """Propiedad para acceder al apellido materno inmutable."""
        return self._apellidoMaterno

    @property
    def telefono(self) -> str:
        """Propiedad para obtener el número de teléfono de contacto."""
        return self._telefono

    @telefono.setter
    def telefono(self, nuevo_telefono: str) -> None:
        """Propiedad setter para actualizar el número de teléfono."""
        self._telefono = nuevo_telefono

    @property
    def correoElectronico(self) -> str:
        """Propiedad para obtener la dirección de correo electrónico."""
        return self._correoElectronico

    @correoElectronico.setter
    def correoElectronico(self, nuevo_correo: str) -> None:
        """Propiedad setter para actualizar la dirección de correo electrónico."""
        self._correoElectronico = nuevo_correo

    # =========================================================================
    # MÉTODOS TRADICIONALES GETTER Y SETTER (Compatibilidad UML / Código Existente)
    # =========================================================================

    def getRut(self) -> str:
        return self._rut

    def getNombres(self) -> str:
        return self._nombres

    def getApellidoPaterno(self) -> str:
        return self._apellidoPaterno

    def getApellidoMaterno(self) -> str:
        return self._apellidoMaterno

    def getTelefono(self) -> str:
        return self._telefono

    def setTelefono(self, telefono: str) -> None:
        self._telefono = telefono

    def getCorreoElectronico(self) -> str:
        return self._correoElectronico

    def setCorreoElectronico(self, correoElectronico: str) -> None:
        self._correoElectronico = correoElectronico

    # =========================================================================
    # MÉTODOS ABSTRACTOS POO
    # =========================================================================

    @abstractmethod
    def getDetallePerfil(self) -> str:
        """Método abstracto: Cada subclase debe definir la presentación de su perfil."""
        return f"{self._nombres} {self._apellidoPaterno} ({self._rut})"

    # =========================================================================
    # MÉTODOS DE VALIDACIÓN DOMINIO (RUT, Teléfono, Email)
    # =========================================================================

    def validarRut(self) -> bool:
        """Valida que el RUT cumpla con el algoritmo de Módulo 11."""
        if not self._rut or not isinstance(self._rut, str):
            return False

        rut_limpio = self._rut.replace(".", "").replace("-", "").replace(" ", "").upper()
        if len(rut_limpio) < 2:
            return False

        cuerpo = rut_limpio[:-1]
        dv_ingresado = rut_limpio[-1]

        if not cuerpo.isdigit():
            return False

        suma = 0
        multiplicador = 2

        for digito in reversed(cuerpo):
            suma += int(digito) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = suma % 11
        resultado = 11 - resto

        if resultado == 11:
            dv_esperado = "0"
        elif resultado == 10:
            dv_esperado = "K"
        else:
            dv_esperado = str(resultado)

        return dv_ingresado == dv_esperado

    def validarTelefono(self) -> bool:
        """Valida formato telefónico (entre 8 y 15 dígitos)."""
        if not self._telefono or not isinstance(self._telefono, str):
            return False
        digitos = re.sub(r"[^0-9]", "", self._telefono)
        return 8 <= len(digitos) <= 15

    def validarCorreoElectronico(self) -> bool:
        """Valida formato de correo electrónico."""
        if not self._correoElectronico or not isinstance(self._correoElectronico, str):
            return False
        patron = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        return bool(re.match(patron, self._correoElectronico))
