"""PowerFit - Productos Suplemento e IndicadorDolar Externo (Requisito #6 UML Profesor)."""
import json
import urllib.request
from datetime import date


class IndicadorDolar:
    """Consulta externa del valor oficial del Dólar (API mindicador.cl)."""

    def __init__(self, fecha: date = None, valorDolar: float = 0.0):
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

    def __init__(self, codigo: str, nombre: str, precioUSD: float, stock: int):
        self._codigo = codigo
        self._nombre = nombre
        self._precioUSD = float(precioUSD)
        self._stock = max(0, int(stock))

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

    def calcularPrecioCLP(self, valorDolar: float) -> float:
        """Calcula el precio final estimado en CLP utilizando la tasa dada."""
        return round(self._precioUSD * valorDolar, 2)

    def hayStock(self, cantidad: int) -> bool:
        """Verifica si existe inventario suficiente para la cantidad solicitada."""
        return self._stock >= cantidad
