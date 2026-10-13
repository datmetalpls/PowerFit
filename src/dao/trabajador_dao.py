# DAO para Trabajador (Administrador, Recepcionista, Instructor)
from typing import List, Optional
from src.dao.conexion import ConexionDB
from src.dao.base_dao import BaseDAO
from src.models.trabajador import Trabajador
from src.models.administrador import Administrador
from src.models.recepcionista import Recepcionista
from src.models.instructor import Instructor
from src.utils.security import GestorSeguridad

class TrabajadorDAO(BaseDAO):
    """Clase encargada del acceso a datos para TRabajador y sus subclases en SQLite"""

    def _map_row_to_trabajador(self, row) -> Trabajador:
        """Convierte una fila de la tabla trabajadores y sus subclases en SQLite"""

        rol = row['rol']
        usr = row['usuario'] if 'usuario' in row.keys() and row['usuario'] else row['nombres'].lower().replace(" ", "")
        pwd = row['pass_hash'] if 'pass_hash' in row.keys() else ''

        datos_base = dict(
            idTrabajador=row['id_trabajador'],
            rut=row['rut'],
            nombres=row['nombres'],
            apellidoPaterno=row['apellido_paterno'],
            apellidoMaterno=row['apellido_materno'],
            telefono=row['telefono'],
            correoElectronico=row['correo_electronico'],
            usuario=usr,
            passHash=pwd
        )
        if rol == 'Administrador':
            t = Administrador(**datos_base, nivelAcceso='General')
        elif rol == 'Instructor':
            t = Instructor(**datos_base, especialidad=row['especialidad'] or 'General')
        else: #Recepcionista o por defecto
            t = Recepcionista(**datos_base)
            
        bloqueado_val = row['cuenta_bloqueada'] if 'cuenta_bloqueada' in row.keys() else 0
        if bool(bloqueado_val):
            t.bloquear()
        return t

    def obtener_todos(self) -> List[Trabajador]:
        """Obtiene todos los trabajadores registrados."""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trabajadores ORDER BY id_trabajador ASC;")
            filas = cursor.fetchall()
            return [self._map_row_to_trabajador(row) for row in filas]

    def obtener_por_rut (self, rut: str) -> Optional[Trabajador]:
        """Busca un trabajador por su RUT"""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trabajadores WHERE rut = ?;", (rut.strip(),))
            row = cursor.fetchone()
            return self._map_row_to_trabajador(row) if row else None


    def obtener_por_id(self, id_entidad: int) -> Optional[Trabajador]:
        """Busca un trabajador por su ID primario"""
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM trabajadores WHERE id_trabajador = ?;", (id_entidad,))
            row = cursor.fetchone()
            return self._map_row_to_trabajador(row) if row else None

    def guardar(self, entidad: Trabajador) -> bool:
        """Inserta o actualiza un trabajador en la base de datos."""
        if isinstance(entidad, Administrador):
            rol = 'Administrador'
        elif isinstance(entidad, Instructor):
            rol = 'Instructor'
        else: 
            rol = 'Recepcionista'

        especialidad = getattr(entidad, 'especialidad', '')
        usr = getattr(entidad, 'usuario', '')
        pwd = getattr(entidad, '_passHash', getattr(entidad, 'passHash', ''))
        # Asegurar que en la persistencia SQLite resida exclusivamente un hash Argon2id válido
        if pwd and not GestorSeguridad.es_hash_argon2(pwd):
            pwd = GestorSeguridad.hashear_password(pwd)
            entidad._passHash = pwd

        id_trab_num = int(entidad.idTrabajador) if str(entidad.idTrabajador).isdigit() else 0

        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            existe = None
            if id_trab_num > 0:
                cursor.execute("SELECT id_trabajador FROM trabajadores WHERE id_trabajador = ?;", (id_trab_num,))
                existe = cursor.fetchone()
            if not existe and entidad.rut:
                cursor.execute("SELECT id_trabajador FROM trabajadores WHERE rut = ?;", (entidad.rut.strip(),))
                existe = cursor.fetchone()

            if existe:
                id_destino = existe['id_trabajador']
                entidad._idTrabajador = str(id_destino)
                cursor.execute("""
                    UPDATE trabajadores
                    SET rut = ?, nombres = ?, apellido_paterno = ?, apellido_materno = ?,
                        telefono = ?, correo_electronico = ?, rol = ?, especialidad = ?,
                        usuario = ?, pass_hash = ?, cuenta_bloqueada = ?
                    WHERE id_trabajador = ?;
                """, (
                    entidad.rut, entidad.nombres, entidad.apellidoPaterno, entidad.apellidoMaterno,
                    entidad.telefono, entidad.correoElectronico, rol, especialidad, usr, pwd, int(entidad.cuenta_bloqueada), id_destino
                ))
            else: 
                cursor.execute("""
                    INSERT INTO trabajadores (rut, nombres, apellido_paterno, apellido_materno, telefono, correo_electronico, rol, especialidad, usuario, pass_hash, cuenta_bloqueada)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                """, (
                    entidad.rut, entidad.nombres, entidad.apellidoPaterno, entidad.apellidoMaterno,
                    entidad.telefono, entidad.correoElectronico, rol, especialidad, usr, pwd, int(entidad.cuenta_bloqueada)
                ))
                if cursor.lastrowid:
                    entidad._idTrabajador = str(cursor.lastrowid)

            conn.commit()
            return True

    @staticmethod
    def migrar_passwords_a_argon2() -> int:
        """
        Migra de forma idempotente todas las contraseñas en texto plano almacenadas en SQLite
        hacia hashes seguros Argon2id.
        Si una contraseña ya es un hash Argon2id, se omite sin re-hashear.
        Retorna la cantidad de registros migrados.
        """
        migrados = 0
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_trabajador, pass_hash FROM trabajadores;")
            filas = cursor.fetchall()
            for f in filas:
                pwd = f['pass_hash'] if 'pass_hash' in f.keys() else ''
                if pwd and not GestorSeguridad.es_hash_argon2(pwd):
                    nuevo_hash = GestorSeguridad.hashear_password(pwd)
                    cursor.execute(
                        "UPDATE trabajadores SET pass_hash = ? WHERE id_trabajador = ?;",
                        (nuevo_hash, f['id_trabajador'])
                    )
                    migrados += 1
            if migrados > 0:
                conn.commit()
        return migrados

    def eliminar(self, id_entidad: int) -> bool:
        """Elimina un trabajador por su ID."""
        with ConexionDB.obt_conexion() as conn: 
            cursor = conn.cursor()
            cursor.execute("DELETE FROM trabajadores WHERE id_trabajador = ?;", (id_entidad,))
            conn.commit()
            return cursor.rowcount > 0