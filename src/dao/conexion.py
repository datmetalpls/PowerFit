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
    def crear_tablas(cls):
        """Crea el esquema inicial de tablas en SQLite si no existen."""
        with cls.obt_conexion() as conexion:
            cursor = conexion.cursor()

            # 1. Tabla Socios
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS socios (
                    id_socio INTEGER PRIMARY KEY AUTOINCREMENT,
                    rut TEXT UNIQUE NOT NULL,
                    nombres TEXT NOT NULL,
                    apellido_paterno TEXT NOT NULL,
                    apellido_materno TEXT DEFAULT '',
                    telefono TEXT DEFAULT '',
                    correo_electronico TEXT DEFAULT '',
                    fecha_vencimiento TEXT NOT NULL,
                    estado_activo INTEGER NOT NULL DEFAULT 1
                );
            """)

            # 2. Tabla Trabajadores (Administrador, Recepcionista, Instructor)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trabajadores (
                    id_trabajador INTEGER PRIMARY KEY AUTOINCREMENT,
                    rut TEXT UNIQUE NOT NULL,
                    nombres TEXT NOT NULL,
                    apellido_paterno TEXT NOT NULL,
                    apellido_materno TEXT DEFAULT '',
                    telefono TEXT DEFAULT '',
                    correo_electronico TEXT DEFAULT '',
                    rol TEXT NOT NULL,
                    especialidad TEXT DEFAULT '',
                    usuario TEXT DEFAULT '',
                    pass_hash TEXT DEFAULT ''
                );
            """)

            # Auto-migrar columnas si la tabla ya existia previamente
            cursor.execute("PRAGMA table_info(trabajadores);")
            columnas_existentes = [col['name'] for col in cursor.fetchall()]
            if 'usuario' not in columnas_existentes:
                cursor.execute("ALTER TABLE trabajadores ADD COLUMN usuario TEXT DEFAULT '';")
            if 'pass_hash' not in columnas_existentes:
                cursor.execute("ALTER TABLE trabajadores ADD COLUMN pass_hash TEXT DEFAULT '';")


            # 3. Tabla Clases
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clases (
                    id_clase INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    horario TEXT NOT NULL,
                    cupo_maximo INTEGER NOT NULL DEFAULT 20,
                    id_instructor INTEGER,
                    FOREIGN KEY (id_instructor) REFERENCES trabajadores(id_trabajador) ON DELETE SET NULL
                );
            """)


            # Auto-migrar columnas si la tabla clases ya existia
            cursor.execute("PRAGMA table_info(clases);")
            columnas_existentes_clases = [col['name'] for col in cursor.fetchall()]
            if 'tipo_disciplina' not in columnas_existentes_clases:
                cursor.execute("ALTER TABLE clases ADD COLUMN tipo_disciplina TEXT DEFAULT '';")
            if 'recurso_fisico' not in columnas_existentes_clases:
                cursor.execute("ALTER TABLE clases ADD COLUMN recurso_fisico INTEGER DEFAULT 0;")
            # 4. Tabla Inscripciones (Relación Socio - Clase)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS inscripciones (
                    id_inscripcion INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_socio INTEGER NOT NULL,
                    id_clase INTEGER NOT NULL,
                    fecha_inscripcion TEXT NOT NULL,
                    asistio INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY (id_socio) REFERENCES socios(id_socio) ON DELETE CASCADE,
                    FOREIGN KEY (id_clase) REFERENCES clases(id_clase) ON DELETE CASCADE,
                    UNIQUE(id_socio, id_clase)
                );
            """)

            # 5. Tabla Suplementos (Punto de Venta)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS suplementos (
                    id_suplemento INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    precio_clp INTEGER NOT NULL,
                    stock INTEGER NOT NULL DEFAULT 0,
                    categoria TEXT DEFAULT 'Proteína'
                );
            """)

            # 6. Tabla Ventas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS ventas (
                    id_venta INTEGER PRIMARY KEY AUTOINCREMENT,
                    numero INTEGER NOT NULL,
                    fecha TEXT NOT NULL,
                    total_clp REAL NOT NULL DEFAULT 0.0
                );
            """)


            # Auto-migrar ventas
            cursor.execute("PRAGMA table_info(ventas);")
            columnas_existentes_ventas = [col['name'] for col in cursor.fetchall()]
            if 'tasa_cambio_usd' not in columnas_existentes_ventas:
                cursor.execute("ALTER TABLE ventas ADD COLUMN tasa_cambio_usd REAL DEFAULT 0.0;")
            # 7. Tabla Detalle Ventas
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS detalles_ventas (
                    id_detalle INTEGER PRIMARY KEY AUTOINCREMENT,
                    id_venta INTEGER NOT NULL,
                    id_suplemento INTEGER NOT NULL,
                    cantidad INTEGER NOT NULL,
                    precio_unitario_clp REAL NOT NULL,
                    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta) ON DELETE CASCADE,
                    FOREIGN KEY (id_suplemento) REFERENCES suplementos(id_suplemento)
                );
            """)

            conexion.commit()

