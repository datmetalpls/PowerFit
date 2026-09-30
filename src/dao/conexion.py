# Módulo de conexión a la base de datos SQLite (powerfit.db)
import sqlite3
from pathlib import Path

RAIZ_PROY=Path(__file__).resolve().parent.parent.parent
DIR_DATABASE = RAIZ_PROY / "database"
DB_PATH = DIR_DATABASE / "powerfit.db"

class ConexionDB:
    """Clase encargada para crear la conexión con SQLITE je"""
    _db_path = DB_PATH

    @classmethod
    def obt_conexion(cls):
        """Crea y retorna una uneva conexion a la base de datos configurada"""

        #1. Nos aseguramosq ue exista la carpeta database
        cls._db_path.parent.mkdir(parents=True, exist_ok=True)

        #2 Vamo a conectar SQLite
        conexion = sqlite3.connect(cls._db_path)

        #3. Configuramos para poder accedr por nombre de columa (ej: fila['nombre'])
        conexion.row_factory = sqlite3.Row

        #4. activamos restricciones / constraints de foráneas. 
        conexion.execute ("PRAGMA foreign_keys = ON;")

        return conexion
    @classmethod
    def crear_tabla(cls):
            """Esquema inicial de tablas en SQLite por si no existen"""
            with cls.obt_conexion() as conexion:
                 cursor=conexion.cursor()
                 #Aquí en adelante se ejecutarán los create table if not exists
                 conexion.commit()
