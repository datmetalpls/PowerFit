# DAO para Suplemento e Inventario
from typing import List, Optional
from src.dao.conexion import ConexionDB
from src.dao.base_dao import BaseDAO
from src.models.suplemento import Suplemento

class SuplementoDAO(BaseDAO):
    """Clase encargada del acceso a datos para la entidad Suplemento en SQLite"""

    def _map_row_to_suplemento(self, row) -> Suplemento:
        """Convierte una fila de la bbdd en un objeto suplemento"""
        # Se mapea precio_clp al modelo POO (precioUSD/CLP)
        suplemento = Suplemento(
            codigo=str(row['id_suplemento']),
            nombre=row['nombre'],
            precioUSD=float(row['precio_clp']),
            stock=row['stock']
        )
        suplemento.categoria = row['categoria'] if 'categoria' in row.keys() else 'General'
        return suplemento

    def obtener_todos(self) -> List[Suplemento]:
        """Obtiene el catálogo completo de suplementos"""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM suplementos ORDER BY id_suplemento ASC;")
            filas = cursor.fetchall()
            return [self._map_row_to_suplemento(row) for row in filas]

    def obtener_por_id(self, id_entidad: int) -> Optional[Suplemento]:
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM suplementos WHERE id_suplemento = ?;", (id_entidad,))
            row = cursor.fetchone()
            return self._map_row_to_suplemento(row) if row else None

    def guardar(self, entidad: Suplemento) -> bool: 
        """Inserta o actualiza un suplemento en la base de datos"""
        categoria = getattr(entidad, 'categoria', 'General')
        precio_clp = int(entidad.precioUSD)

        with ConexionDB.obt_conexion() as conn: 
            cursor = conn.cursor()
            id_sup = int(entidad.codigo) if entidad.codigo.isdigit() else 0
            cursor.execute("SELECT id_suplemento FROM suplementos WHERE id_suplemento = ?;", (id_sup,))
            existe = cursor.fetchone()

            if existe:
                cursor.execute("""
                    UPDATE suplementos
                    SET nombre = ?, precio_clp = ?, stock = ?, categoria = ?
                    WHERE id_suplemento = ?;
                """, (entidad.nombre, precio_clp, entidad.stock, categoria, id_sup))
            else:
                if id_sup > 0:
                    cursor.execute("""
                        INSERT INTO suplementos (id_suplemento, nombre, precio_clp, stock, categoria)
                        VALUES (?, ?, ?, ?, ?);
                    """, (id_sup, entidad.nombre, precio_clp, entidad.stock, categoria))
                else:
                    cursor.execute("""
                        INSERT INTO suplementos (nombre, precio_clp, stock, categoria)
                        VALUES (?, ?, ?, ?);
                    """, (entidad.nombre, precio_clp, entidad.stock, categoria))

            conn.commit()
            return True

    def eliminar(self, id_entidad: int) -> bool: 
        """Elimina un suplemento por su ID"""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM suplementos WHERE id_suplemento = ?;", (id_entidad,))
            conn.commit()
            return cursor.rowcount > 0