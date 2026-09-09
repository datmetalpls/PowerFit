"""Modelo de una venta y sus detalles."""

from datetime import date
from decimal import Decimal
from typing import List

from detalle_venta import DetalleVenta


class Venta:
    """Agrupa los productos o servicios vendidos en una operación."""

    def __init__(self, numero: int, fecha: date, totalCLP: Decimal = Decimal("0")):
        # Función: identificar y fechar la venta.
        # Razón: permite auditar cada operación y conservar su total.
        self.numero = numero
        self.fecha = fecha
        self.totalCLP = Decimal(totalCLP)
        self.detalles: List[DetalleVenta] = []

    def agregarDetalle(self, detalle: DetalleVenta) -> bool:
        # Función: incorporar un detalle y recalcular el total.
        # Razón: una venta debe reflejar todos sus productos registrados.
        if detalle is None or not detalle.confirmarStock():
            return False
        self.detalles.append(detalle)
        self.calcularTotal()
        return True

    def calcularTotal(self) -> Decimal:
        # Función: sumar los subtotales de los detalles.
        # Razón: evita que el total quede desactualizado.
        self.totalCLP = sum(
            (Decimal(detalle.calcularSubtotal()) for detalle in self.detalles),
            Decimal("0"),
        )
        return self.totalCLP
