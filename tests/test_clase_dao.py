import sys
from pathlib import Path

# Agregar raíz del proyecto a sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dao.conexion import ConexionDB
from src.dao.clase_dao import ClaseDAO
from src.models.clase import Spinning, Yoga, Crossfit

def test_crud_clase():
    # 1. Asegurar esquema de tablas
    ConexionDB.crear_tablas()

    # Limpiar clases previas de prueba
    with ConexionDB.obt_conexion() as conn:
        conn.execute("DELETE FROM clases WHERE nombre LIKE 'Test %';")

    dao = ClaseDAO()

    # 2. Crear clases de prueba para distintas disciplinas
    clase_spinning = Spinning(
        codigo="CLS-101",
        nombre="Test Spinning Matutino",
        duracionMin=45,
        cupoMaximo=20,
        sala="Sala 1"
    )

    clase_yoga = Yoga(
        codigo="CLS-102",
        nombre="Test Yoga Relajación",
        duracionMin=60,
        cupoMaximo=15,
        sala="Sala Yoga"
    )

    clase_crossfit = Crossfit(
        codigo="CLS-103",
        nombre="Test Crossfit Avanzado",
        duracionMin=60,
        cupoMaximo=12,
        sala="Box Crossfit"
    )

    # 3. Guardar clases en SQLite
    dao.guardar(clase_spinning)
    dao.guardar(clase_yoga)
    dao.guardar(clase_crossfit)
    print("✅ Clases de prueba guardadas correctamente en SQLite")

    # 4. Leer todas las clases desde SQLite
    todas = dao.obtener_todos()
    print(f"✅ Total de clases registradas en BD: {len(todas)}")
    for c in todas:
        icono = c.obtener_icono_disciplina()
        print(f"   📌 [{c.codigo}] {icono} {c.nombre} - Cupos: {c.cupo_maximo} ({type(c).__name__})")

if __name__ == "__main__":
    test_crud_clase()
