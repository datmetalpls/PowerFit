"""Línea individual de una venta."""

from decimal import Decimal


class DetalleVenta:
    """Calcula cantidad, precio unitario y subtotal de un ítem."""

    def __init__(self, cantidad: int, precioUnitarioCLP: Decimal, stock: int | None = None):
        # Función: guardar los valores necesarios para el cálculo del ítem.
        # Razón: cada línea debe poder auditarse y comprobar su disponibilidad.
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero.")
        if Decimal(precioUnitarioCLP) < 0:
            raise ValueError("El precio no puede ser negativo.")
        if stock is not None and stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        self.cantidad = cantidad
        self.precioUnitarioCLP = Decimal(precioUnitarioCLP)
        self.stock = stock
        self.subtotalCLP = self.calcularSubtotal()

    def calcularSubtotal(self) -> Decimal:
        # Función: multiplicar cantidad por precio unitario.
        # Razón: entrega el importe exacto que compone el total de la venta.
        self.subtotalCLP = self.precioUnitarioCLP * self.cantidad
        return self.subtotalCLP

    def confirmarStock(self) -> bool:
        # Función: verificar que exista stock suficiente para la cantidad.
        # Razón: evita vender unidades que no pueden entregarse.
        return self.stock is None or self.stock >= self.cantidad
