import sys
from pathlib import Path

# Agregar raíz del proyecto a sys.path

sys.path.insert(0, str(Path(__file__). resolve().parent.parent))

from src.dao.conexion import ConexionDB
from src.dao.trabajador_dao import TrabajadorDAO
from src.models.instructor import Instructor
from src.models.administrador import Administrador

def test_crud_trabajador():
    ConexionDB.crear_tablas()

    #Limpiar trabajador previo
    with ConexionDB.obt_conexion() as conn:
        conn.execute("DELETE FROM trabajadores WHERE rut = '22.222.222-2';")

    dao = TrabajadorDAO()

    #Crear instructor de prueba 

    instructor = Instructor(
        idTrabajador="0",
        rut="22.222.222-2",
        nombres="Carlos",
        apellidoPaterno="Gómez",
        apellidoMaterno="Silva",
        telefono="+569998887766",
        correoElectronico="carlos@powerfit.cl",
        especialidad="Crossfit"
    )

    #Guardar en BD
    guardado = dao.guardar(instructor)
    print (f"¿Trabajador Guardaro?: {guardado}")

    #recuperar por rut
    trabajador_db= dao.obtener_por_rut("22.222.222-2")
    if trabajador_db:
        print(f"Total recuperado en BD: {trabajador_db.nombres} ({type(trabajador_db).__name__}) - Especialidad: {getattr(trabajador_db, 'especialidad', 'N/A')}")

    #listar todos los trabajadores
    todos = dao.obtener_todos()
    print(f"Total trabajadores en BD: {len(todos)}")
    
if __name__ == "__main__":
    test_crud_trabajador()