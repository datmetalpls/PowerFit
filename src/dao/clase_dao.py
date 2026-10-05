# DAO para Clase Dirigida (Yoga, Spinning, Crossfit)
from typing import List, Optional
from src.dao.conexion import ConexionDB
from src.dao.base_dao import BaseDAO
from src.models.clase import Clase, ClaseDirigida, Spinning, Yoga, Crossfit
from src.dao.trabajador_dao import TrabajadorDAO

class ClaseDAO(BaseDAO):
    """Clase encargada del acceso a datos para la entidad Clase en SQLite"""

    def __init__(self):
        self._trabajador_dao = TrabajadorDAO()

    def _map_row_to_clase(self, row) -> ClaseDirigida: 
        """Convierte una fila de la BD en un objeto de la subclase concreta de ClaseDirigida."""
        id_instructor = row['id_instructor']
        instructor = self._trabajador_dao.obtener_por_id(id_instructor) if id_instructor else None

        nombre = row['nombre']
        nombre_lower = nombre.lower()
        codigo_str = str(row['id_clase'])
        cupo = row['cupo_maximo']

        if "spinning" in nombre_lower:
            clase = Spinning(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor)
        elif "yoga" in nombre_lower:
            clase = Yoga(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor)
        else:
            clase = Crossfit(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor)

        clase.horario = row['horario']
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

        # Extraer ID numerico de 'entidad.codigo' (ej: 'CLS-001' -> 1)
        cod_str = str(getattr(entidad, 'codigo', '0'))
        id_clase_num = int(''.join(filter(str.isdigit, cod_str)) or '0')

        horario_str = getattr(entidad, 'horario', None) or f"{getattr(entidad, 'duracionMin', 60)} min - {getattr(entidad, 'sala', 'Sala 1')}"

        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_clase FROM clases WHERE id_clase = ?;", (id_clase_num,))
            existe = cursor.fetchone()

            if existe and id_clase_num > 0: 
                cursor.execute("""
                    UPDATE clases
                    SET nombre = ?, horario = ?, cupo_maximo = ?, id_instructor = ?
                    WHERE id_clase = ?;
                """, (entidad.nombre, horario_str, entidad.cupoMaximo, id_instructor, id_clase_num))
            else: 
                cursor.execute("""
                    INSERT INTO clases (nombre, horario, cupo_maximo, id_instructor)
                    VALUES (?, ?, ?, ?);
                """, (entidad.nombre, horario_str, entidad.cupoMaximo, id_instructor))

            conn.commit()
            return True


    def eliminar(self, id_entidad: int) -> bool:
        """Elimina una clase por su ID."""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clases WHERE id_clase = ?;", (id_entidad,))
            conn.commit()
            return cursor.rowcount > 0