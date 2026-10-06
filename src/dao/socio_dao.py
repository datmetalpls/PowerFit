# DAO para Socio
from datetime import datetime, date
from typing import List, Optional
from src.dao.conexion import ConexionDB
from src.dao.base_dao import BaseDAO
from src.models.socio import Socio

class SocioDAO(BaseDAO):
    """Clase encargada del acceso a datos para la entidad Socio en SQLite"""


    def _map_row_to_socio(self, row) -> Socio: 
        """Convierte una fila de la BD SQLite en un objeto Socio del modelo POO."""

        #Convertimos la fecha guardada como exto 'YYYY-MM-DD' a date
        fecha_venc = datetime.strptime(row['fecha_vencimiento'], '%Y-%m-%d').date() if row['fecha_vencimiento'] else None

        return Socio (
        idSocio=row['id_socio'],
        rut=row['rut'],
        nombres=row['nombres'],
        apellidoPaterno=row['apellido_paterno'],
        apellidoMaterno=row['apellido_materno'],
        telefono=row['telefono'],
        correoElectronico=row['correo_electronico'],
        fechaVencimientoMembresia=fecha_venc,
        estadoActivo=bool(row['estado_activo']),
        fechaIngreso=row['fecha_ingreso'] if 'fecha_ingreso' in row.keys() else ''
    )

    def obtener_todos (self) -> List[Socio]:
            """Obtiene lista completa de socios desde la base de datos"""
            with ConexionDB.obt_conexion() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM socios ORDER BY id_socio ASC;")
                filas= cursor.fetchall()
                return [self._map_row_to_socio(row) for row in filas]

    def obtener_por_id(self, id_entidad: int) -> Optional[Socio]:
         """Busca un socio por su ID primario"""
         with ConexionDB.obt_conexion() as conn:
              cursor = conn.cursor()
              cursor.execute("SELECT * FROM socios WHERE id_socio = ?;", (id_entidad,))
              row = cursor.fetchone()
              return self._map_row_to_socio(row) if row else None

    def obtener_por_rut(self, rut: str) -> Optional [Socio]:
         """Busca un socio por su RUT (para validación de torniquete)"""
         with ConexionDB.obt_conexion() as conn:
              cursor = conn.cursor()
              cursor.execute("SELECT * FROM socios WHERE rut = ?;", (rut.strip(),))
              row=cursor.fetchone()
              return self._map_row_to_socio(row) if row else None

    def guardar(self, entidad: Socio) -> bool: 
         """Inserta un nuevo socio o actualiza uno existente (UPSERT)."""
         fecha_str = entidad.fechaVencimientoMembresia.strftime('%Y-%m-%d') if entidad.fechaVencimientoMembresia else None
         with ConexionDB.obt_conexion() as conn: 
              cursor = conn.cursor()

              #Si idSocio==0 o None, o si no existe en la BD -> INSERT, si no -> UPDATE
              cursor.execute("SELECT id_socio from socios WHERE id_socio = ?;", (entidad.idSocio,))
              existe = cursor.fetchone()

              if existe: 
                   cursor.execute("""
                    UPDATE socios
                    SET rut = ?, nombres = ?, apellido_paterno = ?, apellido_materno = ?,
                    telefono =?, correo_electronico = ?, fecha_vencimiento = ?, estado_activo = ?
                    WHERE id_socio = ?;
                   """, (
                        entidad.rut, entidad.nombres, entidad.apellidoPaterno, entidad.apellidoMaterno,
                        entidad.telefono, entidad.correoElectronico, fecha_str,
                        1 if entidad.estadoActivo else 0, entidad.idSocio
                   ))
              else: 
                   cursor.execute("""
                   INSERT INTO socios (rut, nombres, apellido_paterno, apellido_materno, telefono, correo_electronico, fecha_vencimiento, estado_activo, fecha_ingreso)
                    VALUES (?,?,?,?,?,?,?,?, datetime('now', 'localtime'));
                    """,(
                         entidad.rut, entidad.nombres, entidad.apellidoPaterno, entidad.apellidoMaterno,
                         entidad.telefono, entidad.correoElectronico, fecha_str,
                         1 if entidad.estadoActivo else 0
                    ))
              conn.commit()
              return True
    def eliminar (self, id_entidad: int) -> bool:
         """Elimina un socio por su ID primaro."""
         with ConexionDB.obt_conexion() as conn:
              cursor = conn.cursor()
              cursor.execute("DELETE FROM socios WHERE id_socio = ?;", (id_entidad,))
              conn.commit()
              return cursor.rowcount > 0