"""PowerFit - Productos Suplemento, Venta, DetalleVenta e IndicadorDolar (UML posiblediagrama.drawio.xml)."""
import json
import urllib.request
from datetime import date
from typing import List, Optional


class IndicadorDolar:
    """Consulta externa del valor oficial del Dólar (API mindicador.cl)."""

    def __init__(self, fecha: Optional[date] = None, valorDolar: float = 0.0):
        self._fecha = fecha or date.today()
        self._valorDolar = valorDolar

    @property
    def fecha(self) -> date:
        return self._fecha

    @property
    def valorDolar(self) -> float:
        return self._valorDolar

    def obtenerValorDolar(self) -> float:
        """Obtiene el valor actualizado del dólar desde la API o retorna el almacenado."""
        try:
            url = "https://mindicador.cl/api/dolar"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                self._valorDolar = float(data["serie"][0]["valor"])
                self._fecha = date.today()
        except Exception:
            if self._valorDolar == 0.0:
                self._valorDolar = 950.0  # Valor fallback estimado
        return self._valorDolar


class Suplemento:
    """Producto suplemento deportivo con cálculo de precio en CLP según IndicadorDolar."""

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precioUSD: float,
        stock: int,
        stockMinimo: int = 5,
    ):
        self._codigo = codigo
        self._nombre = nombre
        self._precioUSD = float(precioUSD)
        self._stock = max(0, int(stock))
        self._stockMinimo = stockMinimo

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def precioUSD(self) -> float:
        return self._precioUSD

    @property
    def stock(self) -> int:
        return self._stock

    @stock.setter
    def stock(self, nuevo_stock: int):
        self._stock = max(0, nuevo_stock)

    @property
    def stockMinimo(self) -> int:
        return self._stockMinimo

    def calcularPrecioCLP(self, valorDolar: float) -> float:
        """Calcula el precio final estimado en CLP utilizando la tasa dada."""
        return round(self._precioUSD * valorDolar, 2)

    def hayStock(self, cantidad: int) -> bool:
        """Verifica si existe inventario suficiente para la cantidad solicitada."""
        return self._stock >= cantidad

    def descontarStock(self, cantidad: int) -> bool:
        """Descuenta del stock físico si existe suficiente cantidad."""
        if self.hayStock(cantidad):
            self._stock -= cantidad
            return True
        return False


class DetalleVenta:
    """Detalle de una línea de venta asociada a un Suplemento."""

    def __init__(self, cantidad: int, precioUnitarioCLP: float, suplemento: Suplemento):
        self._cantidad = cantidad
        self._precioUnitarioCLP = precioUnitarioCLP
        self._suplemento = suplemento

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @property
    def precioUnitarioCLP(self) -> float:
        return self._precioUnitarioCLP

    @property
    def suplemento(self) -> Suplemento:
        return self._suplemento

    def calcularSubtotal(self) -> float:
        """Calcula el subtotal en CLP para este detalle de venta."""
        return self._cantidad * self._precioUnitarioCLP


class Venta:
    """Representa una transacción de venta compuesta por DetalleVenta."""

    def __init__(self, numero: int, fecha: Optional[date] = None):
        self._numero = numero
        self._fecha = fecha or date.today()
        self._totalCLP = 0.0
        self._detalles: List[DetalleVenta] = []

    @property
    def numero(self) -> int:
        return self._numero

    @property
    def fecha(self) -> date:
        return self._fecha

    @property
    def totalCLP(self) -> float:
        return self._totalCLP

    @property
    def detalles(self) -> List[DetalleVenta]:
        return self._detalles

    def agregarDetalle(self, detalle: DetalleVenta) -> bool:
        """Agrega un detalle de venta y descuenta stock del suplemento."""
        if detalle and detalle.suplemento and detalle.suplemento.descontarStock(detalle.cantidad):
            self._detalles.append(detalle)
            self._totalCLP = self.calcularTotal()
            return True
        return False

    def calcularTotal(self) -> float:
        """Calcula el total general en CLP de la venta."""
        return sum(d.calcularSubtotal() for d in self._detalles)
