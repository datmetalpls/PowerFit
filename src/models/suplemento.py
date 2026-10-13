"""PowerFit - Productos Suplemento, Venta, DetalleVenta e IndicadorDolar (UML posiblediagrama.drawio.xml)."""
import json
import urllib.request
from datetime import date
from pathlib import Path
from typing import List, Optional


class IndicadorDolar:
    """Consulta externa del valor oficial del Dólar (API mindicador.cl) con soporte offline y respaldo."""

    def __init__(self, fecha: Optional[date] = None, valorDolar: float = 0.0):
        self._fecha = fecha or date.today()
        self._valorDolar = valorDolar
        self._es_offline: bool = False
        self._detalle_error: Optional[str] = None

    @property
    def fecha(self) -> date:
        return self._fecha

    @property
    def valorDolar(self) -> float:
        return self._valorDolar

    @property
    def es_offline(self) -> bool:
        """Indica si el valor obtenido proviene del modo de contingencia/respaldo offline."""
        return self._es_offline

    @property
    def detalle_error(self) -> Optional[str]:
        """Contiene el detalle de la excepción si la consulta remota falló."""
        return self._detalle_error

    def obtenerValorDolar(self) -> float:
        """Obtiene el valor del dólar desde la API o recurre a persistencia local / fallback."""
        # Ruta al archivo de respaldo del dólar: database/dolar_backup.txt
        raiz_proyecto = Path(__file__).resolve().parent.parent.parent
        backup_file = raiz_proyecto / "database" / "dolar_backup.txt"

        try:
            url = "https://mindicador.cl/api/dolar"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                data = json.loads(response.read().decode())
                self._valorDolar = float(data["serie"][0]["valor"])
                self._fecha = date.today()
                self._es_offline = False
                self._detalle_error = None

                # 1. Guardar respaldo actualizado en database/dolar_backup.txt
                backup_file.parent.mkdir(parents=True, exist_ok=True)
                with open(backup_file, "w", encoding="utf-8") as f:
                    f.write(str(self._valorDolar))
        except Exception as e:
            self._es_offline = True
            self._detalle_error = str(e)

            # 2. Modo contingencia: Si falla internet, leer database/dolar_backup.txt
            if backup_file.exists():
                try:
                    with open(backup_file, "r", encoding="utf-8") as f:
                        self._valorDolar = float(f.read().strip())
                except Exception:
                    if self._valorDolar == 0.0:
                        self._valorDolar = 950.0
            elif self._valorDolar == 0.0:
                # 3. Fallback estimado final si ni la API ni el archivo existen
                self._valorDolar = 950.0

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
    def id_numerico(self) -> int:
        """Extrae el identificador numérico entero del código del suplemento."""
        digitos = ''.join(filter(str.isdigit, str(self._codigo)))
        return int(digitos) if digitos else 1

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
        if nuevo_stock < 0:
            raise ValueError("El stock de un suplemento no puede ser negativo.")
        self._stock = nuevo_stock

    @property
    def stockMinimo(self) -> int:
        return self._stockMinimo

    def calcularPrecioCLP(self, valorDolar: float) -> float:
        """Calcula el precio final estimado en CLP utilizando la tasa dada."""
        return round(self._precioUSD * valorDolar, 2)

    def hayStock(self, cantidad: int) -> bool:
        """Verifica si existe inventario suficiente para la cantidad solicitada (debe ser > 0)."""
        if cantidad <= 0:
            return False
        return self._stock >= cantidad

    def descontarStock(self, cantidad: int) -> bool:
        """Descuenta del stock físico si la cantidad es positiva y existe suficiente inventario."""
        if cantidad <= 0:
            return False
        if self.hayStock(cantidad):
            self._stock -= cantidad
            return True
        return False


class DetalleVenta:
    """Detalle de una línea de venta asociada a un Suplemento."""

    def __init__(self, cantidad: int, precioUnitarioCLP: float, suplemento: Suplemento):
        if cantidad <= 0:
            raise ValueError(f"La cantidad de venta debe ser estrictamente mayor a cero (recibido: {cantidad}).")
        self._cantidad = int(cantidad)
        self._precioUnitarioCLP = float(precioUnitarioCLP)
        self._suplemento = suplemento

    @property
    def cantidad(self) -> int:
        return self._cantidad

    @cantidad.setter
    def cantidad(self, nueva_cantidad: int):
        if nueva_cantidad <= 0:
            raise ValueError(f"La cantidad debe ser mayor a cero (recibido: {nueva_cantidad}).")
        self._cantidad = int(nueva_cantidad)

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

    @numero.setter
    def numero(self, nuevo_numero: int):
        self._numero = int(nuevo_numero)

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
        if detalle and detalle.cantidad > 0 and detalle.suplemento and detalle.suplemento.descontarStock(detalle.cantidad):
            self._detalles.append(detalle)
            self._totalCLP = self.calcularTotal()
            return True
        return False

    def calcularTotal(self) -> float:
        """Calcula el total general en CLP de la venta."""
        return sum(d.calcularSubtotal() for d in self._detalles)

    def emitirBoleta(
        self,
        cajero: str = "Recepción",
        cliente: str = "Cliente General",
        medio_pago: str = "Tarjeta Débito",
        tasa_dolar: float = 0.0,
    ) -> "Boleta":
        """Genera y retorna la boleta comercial estructurada asociada a esta venta."""
        return Boleta(
            venta=self,
            cajero=cajero,
            cliente=cliente,
            medio_pago=medio_pago,
            tasa_dolar=tasa_dolar,
        )


class Boleta:
    """Representa la boleta electrónica/comprobante fiscal emitido por una Venta."""

    EMPRESA_NOMBRE = "POWERFIT GYM SpA"
    EMPRESA_RUT = "76.432.109-K"
    EMPRESA_GIRO = "Gimnasio y Venta de Suplementos Deportivos"
    EMPRESA_DIRECCION = "Av. Providencia 1234, Santiago, Chile"

    def __init__(
        self,
        venta: Venta,
        cajero: str = "Recepción",
        cliente: str = "Cliente General",
        medio_pago: str = "Tarjeta Débito",
        tasa_dolar: float = 0.0,
        fecha: Optional[str] = None,
    ):
        self._venta = venta
        self._cajero = cajero
        self._cliente = cliente
        self._medio_pago = medio_pago
        self._tasa_dolar = float(tasa_dolar)
        self._fecha_str = fecha

    @property
    def venta(self) -> Venta:
        return self._venta

    @property
    def numero(self) -> int:
        return self._venta.numero

    @property
    def fecha(self) -> date:
        return self._venta.fecha

    @property
    def cajero(self) -> str:
        return self._cajero

    @property
    def cliente(self) -> str:
        return self._cliente

    @property
    def medioPago(self) -> str:
        return self._medio_pago

    @property
    def tasaDolar(self) -> float:
        return self._tasa_dolar

    @property
    def totalCLP(self) -> float:
        return self._venta.totalCLP

    def calcularNeto(self) -> float:
        """Calcula el monto neto antes de IVA (19%)."""
        return round(self.totalCLP / 1.19, 2)

    def calcularIVA(self) -> float:
        """Calcula el monto del IVA (19%)."""
        return round(self.totalCLP - self.calcularNeto(), 2)

    @property
    def fechaFormateada(self) -> str:
        """Retorna la fecha formateada para exhibición fiscal."""
        if self._fecha_str:
            return self._fecha_str
        return self.fecha.strftime("%d/%m/%Y")

    def generarTextoPlano(self) -> str:
        """Genera el contenido de la boleta formateado para ticket térmico estándar."""
        ancho = 52
        linea_doble = "=" * ancho
        linea_simple = "-" * ancho

        lineas = [
            linea_doble,
            f"          🏋️ {self.EMPRESA_NOMBRE}".center(ancho),
            f"RUT: {self.EMPRESA_RUT} | Giro: {self.EMPRESA_GIRO}".center(ancho),
            f"{self.EMPRESA_DIRECCION}".center(ancho),
            linea_doble,
            f" BOLETA ELECTRÓNICA N°: {self.numero:06d}",
            f" FECHA / HORA: {self.fechaFormateada} | EMISIÓN INMEDIATA",
            f" CAJERO(A):    {self.cajero}",
            f" CLIENTE:      {self.cliente}",
            f" FORMA PAGO:   {self.medioPago}",
        ]
        if self._tasa_dolar > 0:
            lineas.append(f" TASA DÓLAR:   ${self._tasa_dolar:,.2f} CLP / USD")

        lineas.extend([
            linea_simple,
            f"{'CANT':<5} {'DESCRIPCIÓN':<23} {'P.UNIT (CLP)':>10} {'TOTAL':>10}",
            linea_simple,
        ])

        for det in self._venta.detalles:
            nombre = det.suplemento.nombre
            if len(nombre) > 23:
                nombre = nombre[:20] + "..."
            subtotal = det.calcularSubtotal()
            lineas.append(
                f"{det.cantidad:<5} {nombre:<23} ${det.precioUnitarioCLP:>9,.0f} ${subtotal:>9,.0f}"
            )

        lineas.extend([
            linea_simple,
            f"{'MONTO NETO:':<35} ${self.calcularNeto():>14,.0f}",
            f"{'I.V.A. (19%):':<35} ${self.calcularIVA():>14,.0f}",
            linea_doble,
            f"{'TOTAL A PAGAR (CLP):':<35} ${self.totalCLP:>14,.0f}",
            linea_doble,
            "¡Gracias por preferir PowerFit Gym!".center(ancho),
            "Comprobante fiscal válido según normativa SII".center(ancho),
            linea_doble,
        ])

        return "\n".join(lineas)

    def generarHTML(self) -> str:
        """Genera un documento HTML optimizado para vista previa e impresión en PDF."""
        filas_html = ""
        for det in self._venta.detalles:
            p_usd = f"${det.suplemento.precioUSD:.2f} USD" if det.suplemento else ""
            filas_html += f"""
            <tr>
                <td style="padding: 6px; text-align: center;">{det.cantidad}</td>
                <td style="padding: 6px;"><b>{det.suplemento.nombre}</b><br><small style="color: #64748B;">{p_usd}</small></td>
                <td style="padding: 6px; text-align: right;">${det.precioUnitarioCLP:,.0f}</td>
                <td style="padding: 6px; text-align: right; font-weight: bold;">${det.calcularSubtotal():,.0f}</td>
            </tr>
            """

        tasa_str = f"<tr><td colspan='2' style='color:#64748B;'>Tasa de Cambio Oficial:</td><td colspan='2' style='text-align:right;'><b>${self._tasa_dolar:,.2f} CLP/USD</b></td></tr>" if self._tasa_dolar > 0 else ""

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{
                    font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                    color: #1E293B;
                    padding: 15px;
                    font-size: 13px;
                }}
                .header {{
                    text-align: center;
                    border-bottom: 2px dashed #CBD5E1;
                    padding-bottom: 12px;
                    margin-bottom: 15px;
                }}
                .header h2 {{ margin: 0; color: #F97316; font-size: 20px; }}
                .header p {{ margin: 3px 0; color: #64748B; font-size: 11px; }}
                .info-box {{
                    background-color: #F8FAFC;
                    border: 1px solid #E2E8F0;
                    border-radius: 6px;
                    padding: 10px;
                    margin-bottom: 15px;
                }}
                .info-box table {{ width: 100%; border-collapse: collapse; font-size: 12px; }}
                .items-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 15px;
                }}
                .items-table th {{
                    background-color: #0F172A;
                    color: #FFFFFF;
                    padding: 8px 6px;
                    font-size: 12px;
                }}
                .items-table td {{ border-bottom: 1px solid #E2E8F0; }}
                .totales-table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 10px;
                }}
                .totales-table td {{ padding: 4px 6px; font-size: 13px; }}
                .total-destacado {{
                    font-size: 16px;
                    font-weight: bold;
                    color: #0F172A;
                    border-top: 2px solid #0F172A;
                    border-bottom: 2px solid #0F172A;
                    padding: 8px 6px !important;
                }}
                .footer {{
                    text-align: center;
                    margin-top: 20px;
                    border-top: 2px dashed #CBD5E1;
                    padding-top: 12px;
                    color: #64748B;
                    font-size: 11px;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🏋️ {self.EMPRESA_NOMBRE}</h2>
                <p><b>RUT: {self.EMPRESA_RUT}</b> | {self.EMPRESA_GIRO}</p>
                <p>{self.EMPRESA_DIRECCION}</p>
                <h3 style="margin: 8px 0 0 0; color: #0F172A;">BOLETA ELECTRÓNICA N° {self.numero:06d}</h3>
            </div>

            <div class="info-box">
                <table>
                    <tr><td><b>Fecha:</b></td><td>{self.fechaFormateada}</td><td><b>Medio de Pago:</b></td><td>{self.medioPago}</td></tr>
                    <tr><td><b>Cajero(a):</b></td><td>{self.cajero}</td><td><b>Cliente:</b></td><td>{self.cliente}</td></tr>
                    {tasa_str}
                </table>
            </div>

            <table class="items-table">
                <thead>
                    <tr>
                        <th style="width: 10%;">Cant</th>
                        <th style="width: 50%; text-align: left;">Descripción</th>
                        <th style="width: 20%; text-align: right;">P. Unit</th>
                        <th style="width: 20%; text-align: right;">Total</th>
                    </tr>
                </thead>
                <tbody>
                    {filas_html}
                </tbody>
            </table>

            <table class="totales-table">
                <tr>
                    <td style="width: 65%; text-align: right; color: #64748B;">Monto Neto:</td>
                    <td style="width: 35%; text-align: right; font-weight: bold;">${self.calcularNeto():,.0f} CLP</td>
                </tr>
                <tr>
                    <td style="text-align: right; color: #64748B;">I.V.A. (19%):</td>
                    <td style="text-align: right; font-weight: bold;">${self.calcularIVA():,.0f} CLP</td>
                </tr>
                <tr class="total-destacado">
                    <td style="text-align: right; color: #F97316;">TOTAL PAGADO:</td>
                    <td style="text-align: right; color: #F97316;">${self.totalCLP:,.0f} CLP</td>
                </tr>
            </table>

            <div class="footer">
                <p><b>¡Muchas gracias por su compra!</b></p>
                <p>Documento tributario electrónico generado por el sistema PowerFit Gym.</p>
            </div>
        </body>
        </html>
        """
        return html

