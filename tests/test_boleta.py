import pytest
from src.models.suplemento import Suplemento, DetalleVenta, Venta, Boleta
from src.dao.venta_dao import VentaDAO
from src.dao.suplemento_dao import SuplementoDAO
from src.dao.conexion import ConexionDB

def test_modelo_boleta_calculos_fiscales():
    """Verifica el cálculo de montos netos, IVA (19%) y total de la boleta."""
    # Suplemento con precio en USD
    sup = Suplemento(codigo="101", nombre="Creatina Creapure 300g", precioUSD=35.0, stock=20)
    
    # Detalle de venta: 2 unidades a $35,000 CLP c/u
    det = DetalleVenta(cantidad=2, precioUnitarioCLP=35000.0, suplemento=sup)
    
    venta = Venta(numero=1)
    venta.agregarDetalle(det)
    
    # Total de la venta = 70,000 CLP
    assert venta.totalCLP == 70000.0
    
    # Emitir boleta a través del método de dominio de Venta
    boleta = venta.emitirBoleta(
        cajero="Recepcionista Test",
        cliente="Juan Pérez (12.345.678-5)",
        medio_pago="Tarjeta Débito",
        tasa_dolar=1000.0
    )
    
    assert isinstance(boleta, Boleta)
    assert boleta.totalCLP == 70000.0
    assert boleta.cajero == "Recepcionista Test"
    assert boleta.cliente == "Juan Pérez (12.345.678-5)"
    assert boleta.medioPago == "Tarjeta Débito"
    assert boleta.tasaDolar == 1000.0
    
    # Desglose fiscal en Chile: Total = Neto + IVA (19%)
    # Neto = 70000 / 1.19 = 58823.53
    # IVA = 70000 - 58823.53 = 11176.47
    neto = boleta.calcularNeto()
    iva = boleta.calcularIVA()
    assert neto == pytest.approx(58823.53, abs=0.01)
    assert iva == pytest.approx(11176.47, abs=0.01)
    assert round(neto + iva, 2) == 70000.0

def test_boleta_generacion_texto_plano_y_html():
    """Verifica que los formatos de ticket térmico y comprobante HTML contengan los datos esenciales."""
    sup = Suplemento(codigo="102", nombre="Whey Protein Isolada 1kg", precioUSD=50.0, stock=15)
    det = DetalleVenta(cantidad=1, precioUnitarioCLP=48000.0, suplemento=sup)
    venta = Venta(numero=42)
    venta.agregarDetalle(det)
    
    boleta = venta.emitirBoleta(
        cajero="Caja Central",
        cliente="Socio VIP",
        medio_pago="Efectivo",
        tasa_dolar=960.0
    )
    
    texto_plano = boleta.generarTextoPlano()
    assert "POWERFIT GYM SpA" in texto_plano
    assert "BOLETA ELECTRÓNICA N°: 000042" in texto_plano
    assert "Whey Protein Isolada" in texto_plano
    assert "48,000" in texto_plano
    assert "TOTAL A PAGAR (CLP):" in texto_plano
    
    html = boleta.generarHTML()
    assert "POWERFIT GYM SpA" in html
    assert "BOLETA ELECTRÓNICA N° 000042" in html
    assert "Caja Central" in html
    assert "Socio VIP" in html
    assert "48,000" in html

def test_persistencia_y_reconstruccion_boleta_dao():
    """Verifica que VentaDAO persista los metadatos de boleta y los reconstruya con fidelidad."""
    ConexionDB.crear_tablas()
    
    sup_dao = SuplementoDAO()
    # Asegurar suplemento de prueba en SQLite
    suplementos = sup_dao.obtener_todos()
    if not suplementos:
        sup_test = Suplemento(codigo="SUP-TEST", nombre="Glutamina 500g", precioUSD=25.0, stock=50)
        sup_dao.guardar(sup_test)
        suplementos = sup_dao.obtener_todos()
        
    primer_sup = suplementos[0]
    
    det = DetalleVenta(cantidad=1, precioUnitarioCLP=25000.0, suplemento=primer_sup)
    venta = Venta(numero=999)
    venta.agregarDetalle(det)
    
    venta_dao = VentaDAO()
    exito = venta_dao.guardar(
        entidad=venta,
        cajero="Cajero BD Test",
        cliente="Cliente Prueba DAO",
        medio_pago="Transferencia"
    )
    assert exito is True
    assert hasattr(venta, 'id_venta_bd')
    assert venta.id_venta_bd is not None
    
    # Probar setter de numero
    venta.numero = venta.id_venta_bd
    assert venta.numero == venta.id_venta_bd
    
    # Reconstruir la boleta desde SQLite
    boleta_recuperada = venta_dao.obtener_boleta_por_id_venta(venta.id_venta_bd)
    assert boleta_recuperada is not None
    assert boleta_recuperada.cajero == "Cajero BD Test"
    assert boleta_recuperada.cliente == "Cliente Prueba DAO"
    assert boleta_recuperada.medioPago == "Transferencia"
    assert boleta_recuperada.totalCLP == 25000.0
    assert len(boleta_recuperada.venta.detalles) >= 1
    assert boleta_recuperada.venta.detalles[0].cantidad == 1
