# DAO para Inscripcion a Clases
from datetime import datetime
from typing import List, Optional
from src.dao.conexion import ConexionDB
from src.dao.base_dao import BaseDAO
from src.dao.socio_dao import SocioDAO
from src.dao.clase_dao import ClaseDAO

class InscripcionDAO(BaseDAO):
    """Clase encargada del acceso a datos para las inscripciones de socios en clases."""

    def __init__(self):
        self._socio_dao = SocioDAO()
        self._clase_dao = ClaseDAO()

    def obtener_inscripciones_por_clase(self, id_clase: int) -> List[dict]:
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_socio, asistio, id_inscripcion FROM inscripciones WHERE id_clase = ? ORDER BY id_inscripcion ASC;", (id_clase,))
            filas = cursor.fetchall()
            return [{'id_socio': row['id_socio'], 'asistio': bool(row['asistio']), 'id_inscripcion': row['id_inscripcion']} for row in filas]

    def obtener_todos(self) -> List[dict]:
        """Obtiene el historial completo de inscripciones."""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inscripciones ORDER BY id_inscripcion ASC;")
            filas = cursor.fetchall()
            
            inscripciones = []
            for row in filas:
                socio = self._socio_dao.obtener_por_id(row['id_socio'])
                clase = self._clase_dao.obtener_por_id(row['id_clase'])
                inscripciones.append({
                    'id_inscripcion': row['id_inscripcion'],
                    'socio': socio,
                    'clase': clase,
                    'fecha_inscripcion': row['fecha_inscripcion'],
                    'asistio': bool(row['asistio'])
                })
            return inscripciones

    def obtener_por_id(self, id_entidad: int) -> Optional[dict]:
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inscripciones WHERE id_inscripcion = ?;", (id_entidad,))
            row = cursor.fetchone()
            if not row:
                return None
            return {
                'id_inscripcion': row['id_inscripcion'],
                'socio': self._socio_dao.obtener_por_id(row['id_socio']),
                'clase': self._clase_dao.obtener_por_id(row['id_clase']),
                'fecha_inscripcion': row['fecha_inscripcion'],
                'asistio': bool(row['asistio'])
            }

    def inscribir_socio(self, id_socio: int, id_clase: int) -> bool:
        """Registra a un socio en una clase dirigida si hay cupo disponible."""
        fecha_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO inscripciones (id_socio, id_clase, fecha_inscripcion, asistio)
                VALUES (?, ?, ?, 0);
            """, (id_socio, id_clase, fecha_str))
            conn.commit()
            return cursor.rowcount > 0

    def marcar_asistencia(self, id_socio: int, id_clase: int, asistio: bool = True) -> bool:
        """Marca o desmarca la asistencia de un socio a una clase."""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE inscripciones
                SET asistio = ?
                WHERE id_socio = ? AND id_clase = ?;
            """, (1 if asistio else 0, id_socio, id_clase))
            conn.commit()
            return cursor.rowcount > 0

    def eliminar_inscripcion_por_relacion(self, id_socio: int, id_clase: int) -> bool:
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inscripciones WHERE id_socio = ? AND id_clase = ?;", (id_socio, id_clase))
            conn.commit()
            return cursor.rowcount > 0

    def guardar(self, entidad: dict) -> bool:
        return self.inscribir_socio(entidad['id_socio'], entidad['id_clase'])

    def eliminar(self, id_entidad: int) -> bool:
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM inscripciones WHERE id_inscripcion = ?;", (id_entidad,))
            conn.commit()
            return cursor.rowcount > 0