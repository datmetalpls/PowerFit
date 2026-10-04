# DAO para Clase Dirigida (Yoga, Spinning, Crossfit)
from typing import List, Optional
from src.dao.conexion import ConexionDB
from src.dao.base_dao import BaseDAO
from src.models.clase import Clase
from src.dao.trabajador_dao import TrabajadorDAO

class ClaseDAO(BaseDAO):
    """Clase encargada del acceso a datos para la entidad Clase en SQLite"""

    def __init__(self):
        self._trabajador_dao = TrabajadorDAO()

    def _map_row_to_clase(self, row) -> Clase: 
        """Convierte una fila de la BD en un objeto Clase."""
        id_instructor = row['id_instructor']
        instructor = self._trabajador_dao.obtener_por_id(id_instructor) if id_instructor else None

        clase = Clase(
            idClase=row['id_clase'],
            nombre=row['nombre'],
            horario=row['horario'],
            cupoMaximo=row['cupo_maximo'],
            instructor=instructor
        )
        return clase

    def obtener_todos(self) -> List[Clase]:
        """Obtiene todas las clases dirigidas registradas."""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clases ORDER BY id_clase ASC;")
            filas = cursor.fetchall()
            return [self._map_row_to_clase(row) for row in filas]

    def obtener_por_id(self, id_entidad: int) -> Optional[Clase]:
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clases WHERE id_clase = ?;", (id_entidad,))
            row = cursor.fetchone()
            return self._map_row_to_clase(row) if row else None

    def guardar(self, entidad: Clase) -> bool:
        """Inserta o actualiza una clase en SQLite."""
        id_instructor = entidad.instructor.idTrabajador if entidad.instructor else None

        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_clase FROM clases WHERE id_clase = ?;", (entidad.idClase,))
            existe = cursor.fetchone()

            if existe: 
                cursor.execute("""
                    UPDATE clases
                    SET nombre = ?, horario = ?, cupo_maximo = ?, id_instructor = ?
                    WHERE id_clase = ?;
                """, (entidad.nombre, entidad.horario, entidad.cupoMaximo, id_instructor, entidad.idClase))
            else: 
                cursor.execute("""
                    INSERT INTO clases (nombre, horario, cupo_maximo, id_instructor)
                    VALUES (?, ?, ?, ?);
                """, (entidad.nombre, entidad.horario, entidad.cupoMaximo, id_instructor))

            conn.commit()
            return True

    def eliminar(self, id_entidad: int) -> bool:
        """Elimina una clase por su ID."""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clases WHERE id_clase = ?;", (id_entidad,))
            conn.commit()
            return cursor.rowcount > 0