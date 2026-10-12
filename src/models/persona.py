"""PowerFit - Modelo Base Abstracto Persona."""
from abc import ABC


class Persona(ABC):
    """Clase abstracta base con validación de RUT por Algoritmo Módulo 11."""

    def __init__(
        self,
        rut: str,
        nombres: str,
        apellidoPaterno: str = "",
        apellidoMaterno: str = "",
        telefono: str = "",
        correoElectronico: str = "",
    ):
        self._rut = rut
        self._nombres = nombres
        self._apellidoPaterno = apellidoPaterno
        self._apellidoMaterno = apellidoMaterno
        self._telefono = telefono
        self._correoElectronico = correoElectronico

    @property
    def rut(self) -> str:
        return self._rut

    @rut.setter
    def rut(self, nuevo_rut: str):
        viejo_rut = self._rut
        self._rut = nuevo_rut
        if not self.validarRut():
            self._rut = viejo_rut
            raise ValueError(f"El RUT '{nuevo_rut}' no es válido.")

    @property
    def nombres(self) -> str:
        return self._nombres

    @nombres.setter
    def nombres(self, nuevo: str):
        self._nombres = nuevo

    @property
    def nombre(self) -> str:
        """Alias 'nombre' exigido por el UML Oficial."""
        if self._apellidoPaterno:
            return f"{self._nombres} {self._apellidoPaterno}"
        return self._nombres

    @property
    def apellidoPaterno(self) -> str:
        return self._apellidoPaterno

    @apellidoPaterno.setter
    def apellidoPaterno(self, nuevo: str):
        self._apellidoPaterno = nuevo

    @property
    def apellidoMaterno(self) -> str:
        return self._apellidoMaterno

    @apellidoMaterno.setter
    def apellidoMaterno(self, nuevo: str):
        self._apellidoMaterno = nuevo

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, nuevo: str):
        self._telefono = nuevo

    @property
    def correoElectronico(self) -> str:
        return self._correoElectronico

    @correoElectronico.setter
    def correoElectronico(self, nuevo: str):
        self._correoElectronico = nuevo

    def getRut(self) -> str:
        return self._rut

    def getNombres(self) -> str:
        return self._nombres

    def getApellidoPaterno(self) -> str:
        return self._apellidoPaterno

    @staticmethod
    def limpiar_rut(rut: str) -> str:
        """Normaliza el RUT eliminando puntos, guiones y espacios en mayúsculas."""
        if not rut or not isinstance(rut, str):
            return ""
        return rut.replace(".", "").replace("-", "").replace(" ", "").upper()

    def coincide_rut(self, rut_comparar: str) -> bool:
        """Compara si el RUT de esta persona coincide con otro RUT ingresado."""
        return self.limpiar_rut(self._rut) == self.limpiar_rut(rut_comparar)

    def validarRut(self) -> bool:
        """Valida la autenticidad del RUT mediante el Algoritmo Módulo 11."""
        rut_limpio = self.limpiar_rut(self._rut)
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
        import re
        if not self._telefono or not isinstance(self._telefono, str):
            return False
        digitos = re.sub(r"[^0-9]", "", self._telefono)
        return 8 <= len(digitos) <= 15

    def validarCorreoElectronico(self) -> bool:
        """Valida formato de correo electrónico."""
        import re
        if not self._correoElectronico or not isinstance(self._correoElectronico, str):
            return False
        patron = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        return bool(re.match(patron, self._correoElectronico))

