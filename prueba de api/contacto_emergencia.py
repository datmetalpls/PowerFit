"""Contacto de emergencia asociado a una persona."""

import re


class ContactoEmergencia:
    """Guarda a quién contactar ante una emergencia."""

    def __init__(self, idContacto: int, nombreCompleto: str, parentesco: str, telefono: str):
        # Función: conservar los datos del contacto alternativo.
        # Razón: permite actuar rápidamente ante incidentes del socio.
        self.idContacto = idContacto
        self.nombreCompleto = nombreCompleto
        self.parentesco = parentesco
        self.telefono = telefono

    def validarTelefono(self) -> bool:
        # Función: comprobar que el teléfono tenga un formato básico válido.
        # Razón: un contacto inválido no serviría durante una emergencia.
        digitos = re.sub(r"[^0-9]", "", self.telefono)
        return 8 <= len(digitos) <= 15
