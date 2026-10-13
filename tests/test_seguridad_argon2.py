"""PowerFit - Pruebas Unitarias de Almacenamiento Seguro de Contraseñas con Argon2id.

Cubre:
1. Inicio de sesión correcto con verificación de hash Argon2id.
2. Contraseña incorrecta rechazada de forma segura.
3. Manejo seguro de hashes inválidos o corruptos sin excepciones no controladas.
4. Transición y migración idempotente de cuentas existentes (ejecución repetida).
5. Usuarios semilla oficiales de demostración (admin, recepcion, instructor).
6. Bloqueo de cuenta tras tres intentos fallidos consecutivos.
"""

import sys
import unittest
from pathlib import Path

# Agregar raíz del proyecto al sys.path
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from src.utils.security import GestorSeguridad
from src.models.administrador import Administrador
from src.models.recepcionista import Recepcionista
from src.models.instructor import Instructor
from src.dao.conexion import ConexionDB
from src.dao.trabajador_dao import TrabajadorDAO


class TestSeguridadArgon2(unittest.TestCase):

    def setUp(self):
        # Asegurar esquema de tablas antes de cada prueba
        ConexionDB.crear_tablas()

    def test_01_inicio_correcto(self):
        """Verifica que una contraseña correcta se autentique exitosamente contra el hash Argon2id."""
        admin = Administrador(
            nivelAcceso="Total",
            idTrabajador="100",
            rut="11.222.333-4",
            nombres="Test Admin",
            usuario="test_admin",
            passHash="ClaveSecreta123"
        )
        self.assertTrue(GestorSeguridad.es_hash_argon2(admin._passHash))
        self.assertTrue(admin.autenticar("ClaveSecreta123"))
        self.assertEqual(admin.intentos_fallidos, 0)
        self.assertFalse(admin.cuenta_bloqueada)

    def test_02_contrasena_incorrecta(self):
        """Verifica que una contraseña errónea sea rechazada e incremente el contador de fallos."""
        recep = Recepcionista(
            idTrabajador="101",
            rut="12.333.444-5",
            nombres="Test Recep",
            usuario="test_recep",
            passHash="PasswordSegura2026"
        )
        self.assertFalse(recep.autenticar("PasswordEquivocada"))
        self.assertEqual(recep.intentos_fallidos, 1)
        self.assertFalse(recep.cuenta_bloqueada)

    def test_03_hash_invalido_o_corrupto(self):
        """Verifica que hashes mal formados o corruptos no generen excepciones y fallen de forma segura."""
        inst = Instructor(
            especialidad="Crossfit",
            idTrabajador="102",
            rut="13.444.555-6",
            nombres="Test Inst",
            usuario="test_inst",
            passHash=""
        )

        # Caso 1: String no relacionado a Argon2
        inst._passHash = "texto_plano_corrupto_sin_formato"
        self.assertFalse(inst.autenticar("cualquier_clave"))
        self.assertEqual(inst.intentos_fallidos, 1)

        # Caso 2: Prefijo aparentemente válido pero payload corrupto
        inst._passHash = "$argon2id$v=19$m=corrupto$$$"
        self.assertFalse(inst.autenticar("cualquier_clave"))
        self.assertEqual(inst.intentos_fallidos, 2)

        # Caso 3: None
        inst._passHash = None
        self.assertFalse(inst.autenticar("cualquier_clave"))
        self.assertEqual(inst.intentos_fallidos, 3)
        self.assertTrue(inst.cuenta_bloqueada)

    def test_04_bloqueo_tres_intentos_fallidos(self):
        """Verifica que la cuenta se bloquee exactamente al alcanzar el 3er intento fallido."""
        admin = Administrador(
            nivelAcceso="Total",
            idTrabajador="103",
            rut="14.555.666-7",
            nombres="Test Bloqueo",
            usuario="test_bloqueo",
            passHash="adminPassword1"
        )

        # Intento 1
        self.assertFalse(admin.autenticar("clave_erronea_1"))
        self.assertEqual(admin.intentos_fallidos, 1)
        self.assertFalse(admin.cuenta_bloqueada)

        # Intento 2
        self.assertFalse(admin.autenticar("clave_erronea_2"))
        self.assertEqual(admin.intentos_fallidos, 2)
        self.assertFalse(admin.cuenta_bloqueada)

        # Intento 3: Se bloquea
        self.assertFalse(admin.autenticar("clave_erronea_3"))
        self.assertEqual(admin.intentos_fallidos, 3)
        self.assertTrue(admin.cuenta_bloqueada)

        # Intento posterior con clave correcta: debe seguir rechazado por cuenta bloqueada
        self.assertFalse(admin.autenticar("adminPassword1"))

        # Desbloqueo administrativo
        admin.desbloquear()
        self.assertFalse(admin.cuenta_bloqueada)
        self.assertEqual(admin.intentos_fallidos, 0)
        self.assertTrue(admin.autenticar("adminPassword1"))

    def test_05_usuarios_semilla(self):
        """Verifica que los usuarios semilla de demostración usen hashes Argon2id y mantengan sus credenciales."""
        dao = TrabajadorDAO()
        cuentas_demo = {
            "admin": "admin123",
            "recepcion": "rec123",
            "instructor": "ins123"
        }

        todos = dao.obtener_todos()
        usuarios_encontrados = {t.usuario: t for t in todos}

        if not all(u in usuarios_encontrados for u in cuentas_demo):
            ConexionDB.reiniciar_base_datos(con_semilla=True)
            todos = dao.obtener_todos()
            usuarios_encontrados = {t.usuario: t for t in todos}

        for usuario, clave in cuentas_demo.items():
            self.assertIn(usuario, usuarios_encontrados, f"Usuario semilla '{usuario}' no encontrado en BD")
            t = usuarios_encontrados[usuario]
            # Verificar formato del hash en el modelo y persistencia
            self.assertTrue(
                GestorSeguridad.es_hash_argon2(t._passHash),
                f"El usuario '{usuario}' no posee un hash Argon2id válido."
            )
            self.assertTrue(
                t.autenticar(clave),
                f"La autenticación falló para el usuario semilla '{usuario}' con clave '{clave}'."
            )

    def test_06_migracion_idempotente_cuentas_existentes(self):
        """Verifica que cuentas existentes con contraseñas en texto plano se migren a Argon2id de forma idempotente."""
        with ConexionDB.obt_conexion() as conn:
            conn.execute("DELETE FROM trabajadores WHERE usuario = 'cuenta_antigua';")
            conn.execute("""
                INSERT INTO trabajadores (rut, nombres, apellido_paterno, apellido_materno, rol, usuario, pass_hash)
                VALUES ('19.888.777-6', 'Usuario', 'Antiguo', '', 'Recepcionista', 'cuenta_antigua', 'clavePlana123');
            """)
            conn.commit()

        # 1. Primera ejecución de la migración
        migrados_primera = TrabajadorDAO.migrar_passwords_a_argon2()
        self.assertGreaterEqual(migrados_primera, 1)

        dao = TrabajadorDAO()
        t = dao.obtener_por_rut("19.888.777-6")
        self.assertIsNotNone(t)
        self.assertTrue(GestorSeguridad.es_hash_argon2(t._passHash))
        self.assertTrue(t.autenticar("clavePlana123"))

        hash_generado = t._passHash

        # 2. Segunda ejecución de la migración (debe ser idempotente, 0 modificaciones)
        migrados_segunda = TrabajadorDAO.migrar_passwords_a_argon2()
        self.assertEqual(migrados_segunda, 0)

        # 3. Comprobar que el hash no haya mutado ni sido re-hasheado
        t_verificado = dao.obtener_por_rut("19.888.777-6")
        self.assertEqual(t_verificado._passHash, hash_generado)
        self.assertTrue(t_verificado.autenticar("clavePlana123"))

        # Limpieza
        with ConexionDB.obt_conexion() as conn:
            conn.execute("DELETE FROM trabajadores WHERE usuario = 'cuenta_antigua';")
            conn.commit()


if __name__ == "__main__":
    unittest.main()
