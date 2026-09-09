"""Indicador del valor del dólar usado para convertir precios."""

from datetime import date
from decimal import Decimal


class IndicadorDolar:
    """Conserva el valor del dólar correspondiente a una fecha."""

    def __init__(self, fecha: date, valorCLP: Decimal):
        # Función: guardar la fecha y el valor de conversión.
        # Razón: permite calcular precios reproducibles en moneda local.
        if Decimal(valorCLP) <= 0:
            raise ValueError("El valor del dólar debe ser positivo.")
        self.fecha = fecha
        self.valorCLP = Decimal(valorCLP)

    def obtenerValor(self) -> Decimal:
        # Función: devolver el valor vigente registrado.
        # Razón: otros objetos necesitan consultar la tasa de conversión.
        return self.valorCLP

    def actualizarValor(self, nuevoValor: Decimal) -> None:
        # Función: actualizar la tasa del indicador.
        # Razón: el precio del dólar cambia y debe mantenerse vigente.
        if Decimal(nuevoValor) <= 0:
            raise ValueError("El valor del dólar debe ser positivo.")
        self.valorCLP = Decimal(nuevoValor)
        self.fecha = date.today()
