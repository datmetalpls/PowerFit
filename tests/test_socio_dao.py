import sys
from pathlib import Path

# Agregar raíz del proyecto a sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from datetime import date
from src.dao.conexion import ConexionDB
from src.dao.socio_dao import SocioDAO
from src.models.socio import Socio

    
def test_crud_socio():
    # 1. Asegurar tablas creadas
    ConexionDB.crear_tablas()

    # Limpiar socios previos del test
    with ConexionDB.obt_conexion() as conn:
        conn.execute("DELETE FROM socios WHERE rut = '11.111.111-1';")

    dao = SocioDAO()

    # 2. Crear socio de prueba
    socio = Socio(
        idSocio=0,
        rut="11.111.111-1",
        nombres="Juan",
        apellidoPaterno="Pérez",
        apellidoMaterno="Cotapos",
        telefono="+56912345678",
        correoElectronico="juan@powerfit.cl",
        fechaVencimientoMembresia=date(2026, 12, 31),
        estadoActivo=True
    )

    # 3. Guardar en SQLite
    guardado = dao.guardar(socio)
    print(f"¿Guardado exitoso?: {guardado}")

    # 4. Obtener por RUT
    socio_db = dao.obtener_por_rut("11.111.111-1")
    if socio_db:
        print(f"Socio recuperado de la BD: {socio_db.nombres} {socio_db.apellidoPaterno} - RUT: {socio_db.rut}")

    # 5. Listar todos
    todos = dao.obtener_todos()
    print(f"Total de socios en BD: {len(todos)}")

if __name__ == "__main__":
    test_crud_socio()