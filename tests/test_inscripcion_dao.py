import sys
from pathlib import Path
from datetime import date

# Agregar raíz del proyecto a sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dao.conexion import ConexionDB
from src.dao.socio_dao import SocioDAO
from src.dao.clase_dao import ClaseDAO
from src.dao.inscripcion_dao import InscripcionDAO
from src.models.socio import Socio
from src.models.clase import Spinning

def test_crud_inscripcion():
    # 1. Asegurar tablas
    ConexionDB.crear_tablas()

    socio_dao = SocioDAO()
    clase_dao = ClaseDAO()
    inscripcion_dao = InscripcionDAO()

    # 2. Crear socio y clase para la prueba
    socio_test = Socio(
        idSocio=0,
        rut="99.999.999-9",
        nombres="SocioInscripcion",
        apellidoPaterno="Test",
        fechaVencimientoMembresia=date(2026, 12, 31),
        estadoActivo=True
    )
    socio_dao.guardar(socio_test)
    socio_db = socio_dao.obtener_por_rut("99.999.999-9")

    clase_test = Spinning(codigo="CLS-999", nombre="Test Spinning Inscripcion", cupoMaximo=15, sala="Sala 1")
    clase_dao.guardar(clase_test)
    clases = clase_dao.obtener_todos()
    clase_db = next((c for c in clases if c.nombre == "Test Spinning Inscripcion"), None)

    if socio_db and clase_db:
        id_clase_num = int(''.join(filter(str.isdigit, clase_db.codigo)) or '1')
        
        # 3. Inscribir socio en SQLite
        exito_ins = inscripcion_dao.inscribir_socio(socio_db.idSocio, id_clase_num)
        print(f"✅ Socio inscrito en clase: {exito_ins}")

        # 4. Marcar asistencia en SQLite
        exito_asist = inscripcion_dao.marcar_asistencia(socio_db.idSocio, id_clase_num, asistio=True)
        print(f"✅ Asistencia de socio registrada en SQLite: {exito_asist}")

        # 5. Consultar inscripciones
        todas = inscripcion_dao.obtener_todos()
        print(f"✅ Total inscripciones registradas en BD: {len(todas)}")

if __name__ == "__main__":
    test_crud_inscripcion()
