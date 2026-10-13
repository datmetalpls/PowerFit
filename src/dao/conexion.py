# Módulo de conexión a la base de datos SQLite (powerfit.db)
import sqlite3
from pathlib import Path

RAIZ_PROY=Path(__file__).resolve().parent.parent.parent
DIR_DATABASE = RAIZ_PROY / "database"
DB_PATH = DIR_DATABASE / "powerfit.db"

class ConexionDB:
    """Clase encargada de gestionar la conexión con la base de datos SQLite."""
    _db_path = DB_PATH

    @classmethod
    def obt_conexion(cls):
        """Crea y retorna una nueva conexión a la base de datos configurada."""
        # 1. Asegurar que exista la carpeta database
        cls._db_path.parent.mkdir(parents=True, exist_ok=True)

        # 2. Conectar a SQLite
        conexion = sqlite3.connect(cls._db_path)

        # 3. Configurar acceso por nombre de columna (ej: fila['nombre'])
        conexion.row_factory = sqlite3.Row

        # 4. Activar restricciones de claves foráneas
        conexion.execute("PRAGMA foreign_keys = ON;")

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
                    estado_activo INTEGER NOT NULL DEFAULT 1,
                    fecha_ingreso TEXT DEFAULT (datetime('now', 'localtime'))
                );
            """)

            cursor.execute("PRAGMA table_info(socios);")
            columnas_existentes = [col['name'] for col in cursor.fetchall()]
            if 'fecha_ingreso' not in columnas_existentes:
                cursor.execute("ALTER TABLE socios ADD COLUMN fecha_ingreso TEXT;")

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
                    pass_hash TEXT DEFAULT '',
                    cuenta_bloqueada INTEGER DEFAULT 0
                );
            """)

            # Auto-migrar columnas si la tabla ya existia previamente
            cursor.execute("PRAGMA table_info(trabajadores);")
            columnas_existentes = [col['name'] for col in cursor.fetchall()]
            if 'usuario' not in columnas_existentes:
                cursor.execute("ALTER TABLE trabajadores ADD COLUMN usuario TEXT DEFAULT '';")
            if 'pass_hash' not in columnas_existentes:
                cursor.execute("ALTER TABLE trabajadores ADD COLUMN pass_hash TEXT DEFAULT '';")
            if 'cuenta_bloqueada' not in columnas_existentes:
                cursor.execute("ALTER TABLE trabajadores ADD COLUMN cuenta_bloqueada INTEGER DEFAULT 0;")


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

        # Ejecutar migración idempotente de contraseñas de trabajadores a Argon2id
        cls.migrar_passwords_a_argon2()

    @classmethod
    def migrar_passwords_a_argon2(cls) -> int:
        """Migra de forma idempotente las contraseñas en texto plano almacenadas en la BD a Argon2id."""
        from src.dao.trabajador_dao import TrabajadorDAO
        return TrabajadorDAO.migrar_passwords_a_argon2()

    @classmethod
    def reiniciar_tablas(cls):
        """Elimina y vuelve a crear todas las tablas en SQLite desde cero."""
        tablas = [
            "detalles_ventas",
            "ventas",
            "inscripciones",
            "suplementos",
            "clases",
            "trabajadores",
            "socios",
        ]
        with cls.obt_conexion() as conexion:
            cursor = conexion.cursor()
            for tabla in tablas:
                cursor.execute(f"DROP TABLE IF EXISTS {tabla};")
            conexion.commit()
        cls.crear_tablas()

    @classmethod
    def poblar_datos_semilla(cls):
        """Puebla la base de datos con datos semilla oficiales para pruebas y demostraciones."""
        from src.dao.trabajador_dao import TrabajadorDAO
        from src.dao.socio_dao import SocioDAO
        from src.dao.clase_dao import ClaseDAO
        from src.models import (
            Administrador,
            Recepcionista,
            Instructor,
            Socio,
            ClaseSpinning,
            ClaseYoga,
            ClaseCrossfit,
        )

        trab_dao = TrabajadorDAO()
        socio_dao = SocioDAO()
        clase_dao = ClaseDAO()

        # 1. Personal del sistema (3 roles estándar con credenciales oficiales)
        admin = Administrador(
            nivelAcceso="Total",
            idTrabajador="0",
            rut="11.111.111-1",
            nombres="Administrador General",
            apellidoPaterno="PowerFit",
            usuario="admin",
            passHash="admin123",
        )
        recep = Recepcionista(
            idTrabajador="0",
            rut="12.345.678-5",
            nombres="Carolina",
            apellidoPaterno="Silva",
            apellidoMaterno="Rojas",
            usuario="recepcion",
            passHash="rec123",
            turno="Mañana",
        )
        inst = Instructor(
            especialidad="Fitness & Crossfit",
            idTrabajador="0",
            rut="14.805.293-K",
            nombres="Carlos",
            apellidoPaterno="Montero",
            apellidoMaterno="Díaz",
            usuario="instructor",
            passHash="ins123",
        )
        for t in [admin, recep, inst]:
            trab_dao.guardar(t)

        # 2. Socios de prueba (3 casos preparados para simulación de torniquete)
        socio_al_dia = Socio.crear_con_estado(
            idSocio=0,
            rut="18.045.022-K",
            nombres="Juan Carlos",
            apellidoPaterno="Pérez",
            apellidoMaterno="González",
            telefono="912345678",
            correoElectronico="juan.perez@powerfit.cl",
            tipo_estado="Al Día",
        )
        socio_vencido = Socio.crear_con_estado(
            idSocio=0,
            rut="15.555.555-5",
            nombres="María Ignacia",
            apellidoPaterno="Soto",
            apellidoMaterno="Valenzuela",
            telefono="987654321",
            correoElectronico="maria.soto@powerfit.cl",
            tipo_estado="Vencida",
        )
        socio_cancelado = Socio.crear_con_estado(
            idSocio=0,
            rut="16.666.666-6",
            nombres="Pedro Pablo",
            apellidoPaterno="Gómez",
            apellidoMaterno="Lagos",
            telefono="955554433",
            correoElectronico="pedro.gomez@powerfit.cl",
            tipo_estado="Cancelado",
        )
        for s in [socio_al_dia, socio_vencido, socio_cancelado]:
            socio_dao.guardar(s)

        # 3. Clases dirigidas (3 disciplinas con salas y cupos)
        c_spinning = ClaseSpinning(
            codigo="1",
            nombre="Spinning Matutino",
            cupoMaximo=20,
            duracionMin=45,
            sala="Sala Spinning",
        )
        c_yoga = ClaseYoga(
            codigo="2",
            nombre="Yoga Relajación",
            cupoMaximo=15,
            duracionMin=60,
            sala="Sala Yoga",
        )
        c_crossfit = ClaseCrossfit(
            codigo="3",
            nombre="Crossfit Avanzado",
            cupoMaximo=12,
            duracionMin=60,
            sala="Box Crossfit",
        )
        for c in [c_spinning, c_yoga, c_crossfit]:
            clase_dao.guardar(c)

        # 4. Catálogo de suplementos deportivos (10 productos)
        catalogo = [
            ("Proteína Whey Gold 100% 1kg", 45000, 50, "Proteína"),
            ("Creatina Monohidratada 500g", 25000, 40, "Fuerza"),
            ("Pre-Entreno C4 Explosive 300g", 30000, 35, "Energía"),
            ("BCAA Aminoácidos 2:1:1 400g", 20000, 30, "Recuperación"),
            ("Quemador de Grasa Lipo-6 120 cap", 35000, 25, "Definición"),
            ("Ganador de Masa Serious Mass 2.5kg", 55000, 20, "Volumen"),
            ("Multivitamínico Opti-Men 90 tab", 22000, 45, "Salud"),
            ("Barras de Proteína (Caja x12)", 28000, 60, "Snack"),
            ("Shaker Metálico PowerFit 700ml", 12000, 50, "Accesorios"),
            ("Glutamina Micronizada 300g", 18000, 30, "Recuperación"),
        ]
        with cls.obt_conexion() as conn:
            cursor = conn.cursor()
            for nombre, precio, stock, cat in catalogo:
                cursor.execute("""
                    INSERT INTO suplementos (nombre, precio_clp, stock, categoria)
                    VALUES (?, ?, ?, ?);
                """, (nombre, precio, stock, cat))
            conn.commit()

    @classmethod
    def reiniciar_base_datos(cls, con_semilla: bool = True):
        """Reinicia la base de datos a cero y opcionalmente inserta los datos semilla."""
        cls.reiniciar_tablas()
        if con_semilla:
            cls.poblar_datos_semilla()

