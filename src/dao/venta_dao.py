# DAO para Venta y DetalleVenta
from typing import List, Optional
from datetime import datetime
from src.dao.conexion import ConexionDB
from src.dao.base_dao import BaseDAO
from src.models.suplemento import Venta

class VentaDAO(BaseDAO):
    """Clase encargada del acceso a datos para las Ventas en SQLite."""

    def obtener_todos(self) -> List[dict]:
        """Obtiene todas las ventas registradas con sus detalles y suplementos."""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.id_venta, v.numero, v.fecha, v.total_clp, v.tasa_cambio_usd,
                       v.medio_pago, v.cajero, v.cliente,
                       dv.id_suplemento, dv.cantidad, dv.precio_unitario_clp,
                       s.nombre AS nombre_suplemento, s.precio_clp AS precio_usd_suplemento
                FROM ventas v
                LEFT JOIN detalles_ventas dv ON v.id_venta = dv.id_venta
                LEFT JOIN suplementos s ON dv.id_suplemento = s.id_suplemento
                ORDER BY v.id_venta ASC;
            """)
            filas = cursor.fetchall()
            ventas = []
            for row in filas:
                ventas.append({
                    "id_venta": row['id_venta'],
                    "numero": row['numero'],
                    "fecha": row['fecha'],
                    "total_clp": row['total_clp'],
                    "tasa_cambio_usd": row['tasa_cambio_usd'] or 0.0,
                    "medio_pago": row['medio_pago'] if 'medio_pago' in row.keys() and row['medio_pago'] else "Tarjeta Débito",
                    "cajero": row['cajero'] if 'cajero' in row.keys() and row['cajero'] else "Recepción",
                    "cliente": row['cliente'] if 'cliente' in row.keys() and row['cliente'] else "Cliente General",
                    "nombre_producto": row['nombre_suplemento'] or "Suplemento",
                    "cantidad": row['cantidad'] or 0,
                    "precio_unitario": row['precio_unitario_clp'] or 0.0,
                    "precio_usd": row['precio_usd_suplemento'] or 0.0,
                })
            return ventas

    def obtener_por_id(self, id_entidad: int) -> Optional[dict]:
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ventas WHERE id_venta = ?;", (id_entidad,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def obtener_boleta_por_id_venta(self, id_venta: int) -> Optional["Boleta"]:
        """Reconstruye una Venta completa con sus DetalleVenta desde SQLite y retorna su Boleta."""
        from src.models.suplemento import Suplemento, DetalleVenta, Boleta
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ventas WHERE id_venta = ?;", (id_venta,))
            v_row = cursor.fetchone()
            if not v_row:
                return None

            cursor.execute("""
                SELECT dv.*, s.nombre, s.precio_clp AS precio_usd
                FROM detalles_ventas dv
                JOIN suplementos s ON dv.id_suplemento = s.id_suplemento
                WHERE dv.id_venta = ?;
            """, (id_venta,))
            det_filas = cursor.fetchall()

            venta = Venta(numero=v_row['numero'])
            for df in det_filas:
                sup = Suplemento(
                    codigo=str(df['id_suplemento']),
                    nombre=df['nombre'],
                    precioUSD=float(df['precio_usd']),
                    stock=999  # stock dummy solo para reconstrucción del comprobante
                )
                det = DetalleVenta(
                    cantidad=df['cantidad'],
                    precioUnitarioCLP=float(df['precio_unitario_clp']),
                    suplemento=sup
                )
                venta._detalles.append(det)

            venta._totalCLP = float(v_row['total_clp'])
            medio_pago = v_row['medio_pago'] if 'medio_pago' in v_row.keys() and v_row['medio_pago'] else "Tarjeta Débito"
            cajero = v_row['cajero'] if 'cajero' in v_row.keys() and v_row['cajero'] else "Recepción"
            cliente = v_row['cliente'] if 'cliente' in v_row.keys() and v_row['cliente'] else "Cliente General"
            tasa_usd = float(v_row['tasa_cambio_usd']) if 'tasa_cambio_usd' in v_row.keys() and v_row['tasa_cambio_usd'] else 0.0

            return Boleta(
                venta=venta,
                cajero=cajero,
                cliente=cliente,
                medio_pago=medio_pago,
                tasa_dolar=tasa_usd,
                fecha=str(v_row['fecha']),
            )

    def guardar(
        self,
        entidad: Venta,
        cajero: str = "Recepción",
        cliente: str = "Cliente General",
        medio_pago: str = "Tarjeta Débito"
    ) -> bool:
        """Guarda la venta y sus detalles en SQLite con trazabilidad de boleta."""
        fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tasa_usd = 0.0
        if entidad.detalles and entidad.detalles[0].suplemento.precioUSD > 0:
            tasa_usd = entidad.detalles[0].precioUnitarioCLP / entidad.detalles[0].suplemento.precioUSD

        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ventas (numero, fecha, total_clp, tasa_cambio_usd, medio_pago, cajero, cliente)
                VALUES (?, ?, ?, ?, ?, ?, ?);
            """, (entidad.numero, fecha_str, entidad.totalCLP, tasa_usd, medio_pago, cajero, cliente))
            id_venta = cursor.lastrowid
            entidad.id_venta_bd = id_venta

            for det in entidad.detalles:
                if det.cantidad <= 0:
                    raise ValueError(f"No se puede registrar una venta con cantidad no positiva ({det.cantidad}).")
                if hasattr(det.suplemento, 'id_numerico') and det.suplemento.id_numerico:
                    id_sup = int(det.suplemento.id_numerico)
                elif det.suplemento.codigo.isdigit():
                    id_sup = int(det.suplemento.codigo)
                else:
                    id_sup = 1
                cursor.execute("""
                    INSERT INTO detalles_ventas (id_venta, id_suplemento, cantidad, precio_unitario_clp)
                    VALUES (?, ?, ?, ?);
                """, (id_venta, id_sup, det.cantidad, det.precioUnitarioCLP))
                
                # Descontar stock
                cursor.execute("""
                    UPDATE suplementos SET stock = stock - ? WHERE id_suplemento = ?;
                """, (det.cantidad, id_sup))

            conn.commit()
            return True

    def eliminar(self, id_entidad: int) -> bool:
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ventas WHERE id_venta = ?;", (id_entidad,))
            conn.commit()
            return cursor.rowcount > 0
