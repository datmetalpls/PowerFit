"""Modelo de una comuna disponible para las direcciones del gimnasio."""


class Comuna:
    """Representa una comuna que puede habilitarse o deshabilitarse."""

    def __init__(self, idComuna: int, nombre: str, activo: bool = True):
        # Función: guardar la identidad y estado de la comuna.
        # Razón: las direcciones necesitan asociarse a una comuna vigente.
        self.idComuna = idComuna
        self.nombre = nombre
        self.activo = activo

    def registrar(self) -> None:
        # Función: activar la comuna en el catálogo.
        # Razón: permite disponer de ella para nuevos registros.
        self.activo = True

    def actualizar(self, nombre: str) -> None:
        # Función: actualizar el nombre de la comuna.
        # Razón: mantiene correcto el catálogo administrativo.
        self.nombre = nombre

    def desactivar(self) -> None:
        # Función: marcar la comuna como inactiva.
        # Razón: evita usarla sin borrar su historial.
        self.activo = False
