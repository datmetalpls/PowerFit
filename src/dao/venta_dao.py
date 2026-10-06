# DAO para Venta y DetalleVenta
from typing import List, Optional
from datetime import datetime
from src.dao.conexion import ConexionDB
from src.dao.base_dao import BaseDAO
from src.models.suplemento import Venta, DetalleVenta, Suplemento

class VentaDAO(BaseDAO):
    """Clase encargada del acceso a datos para las Ventas en SQLite."""

    def obtener_todos(self) -> List[dict]:
        """Obtiene todas las ventas registradas con sus detalles y suplementos."""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT v.id_venta, v.numero, v.fecha, v.total_clp, v.tasa_cambio_usd,
                       dv.id_suplemento, dv.cantidad, dv.precio_unitario_clp,
                       s.nombre AS nombre_suplemento
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
                    "nombre_producto": row['nombre_suplemento'] or "Suplemento",
                    "cantidad": row['cantidad'] or 0,
                    "precio_unitario": row['precio_unitario_clp'] or 0.0
                })
            return ventas

    def obtener_por_id(self, id_entidad: int) -> Optional[dict]:
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM ventas WHERE id_venta = ?;", (id_entidad,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def guardar(self, entidad: Venta) -> bool:
        """Guarda la venta y sus detalles en SQLite."""
        fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Extract tasa_cambio_usd (which is stored in suplemento for today)
        tasa_usd = 0.0
        if entidad.detalles:
            tasa_usd = entidad.detalles[0].precioUnitarioCLP / entidad.detalles[0].suplemento.precioUSD if entidad.detalles[0].suplemento.precioUSD > 0 else 0.0

        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO ventas (numero, fecha, total_clp, tasa_cambio_usd)
                VALUES (?, ?, ?, ?);
            """, (entidad.numero, fecha_str, entidad.totalCLP, tasa_usd))
            id_venta = cursor.lastrowid

            for det in entidad.detalles:
                id_sup = int(det.suplemento.codigo) if det.suplemento.codigo.isdigit() else 1
                cursor.execute("""
                    INSERT INTO detalles_ventas (id_venta, id_suplemento, cantidad, precio_unitario_clp)
                    VALUES (?, ?, ?, ?);
                """, (id_venta, id_sup, det.cantidad, det.precioUnitarioCLP))
                
                # Descontar stock (Point 4)
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
