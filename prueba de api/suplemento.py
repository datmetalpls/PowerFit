"""Producto de suplemento vendido por el gimnasio."""

from decimal import Decimal


class Suplemento:
    """Producto con stock y precio expresado en dólares."""

    def __init__(self, codigo: int, nombre: str, stock: int, precioUSD: Decimal):
        # Función: guardar la identificación, existencia y precio del producto.
        # Razón: inventario y ventas necesitan una fuente única de información.
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")
        if Decimal(precioUSD) < 0:
            raise ValueError("El precio no puede ser negativo.")
        self.codigo = codigo
        self.nombre = nombre
        self.stock = stock
        self.precioUSD = Decimal(precioUSD)

    def hayStock(self) -> bool:
        # Función: comprobar si queda al menos una unidad.
        # Razón: evita ofrecer productos agotados.
        return self.stock > 0

    def descontarStock(self, cantidad: int = 1) -> bool:
        # Función: reducir existencias después de una venta.
        # Razón: mantiene el inventario sincronizado con las salidas.
        if cantidad <= 0 or self.stock < cantidad:
            return False
        self.stock -= cantidad
        return True

    def calcularPrecioCLP(self, valorDolar: Decimal) -> Decimal:
        # Función: convertir el precio desde USD a CLP.
        # Razón: las ventas del gimnasio se registran en pesos chilenos.
        return self.precioUSD * Decimal(valorDolar)
