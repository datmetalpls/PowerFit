import sys
from pathlib import Path

# Agregar raíz del proyecto a sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.dao.conexion import ConexionDB
from src.dao.suplemento_dao import SuplementoDAO
from src.models.suplemento import Suplemento

def test_crud_suplemento():
    # 1. Asegurar esquema de tablas
    ConexionDB.crear_tablas()

    # Limpiar suplementos de prueba previas y sus detalles asociados
    with ConexionDB.obt_conexion() as conn:
        conn.execute("DELETE FROM detalles_ventas WHERE id_suplemento IN (SELECT id_suplemento FROM suplementos WHERE nombre LIKE 'Test %');")
        conn.execute("DELETE FROM suplementos WHERE nombre LIKE 'Test %';")

    dao = SuplementoDAO()

    # 2. Crear suplementos de prueba
    sup_whey = Suplemento(codigo="1", nombre="Test Proteína Whey Gold 1kg", precioUSD=45.0, stock=50)
    sup_creatina = Suplemento(codigo="2", nombre="Test Creatina Monohidratada 500g", precioUSD=25.0, stock=30)

    # 3. Guardar en SQLite
    dao.guardar(sup_whey)
    dao.guardar(sup_creatina)
    print("✅ Suplementos guardados correctamente en SQLite")

    # 4. Probar reposición y descuento de stock
    sup_whey.descontarStock(5)
    dao.guardar(sup_whey)

    # 5. Obtener todos los suplementos
    todos = dao.obtener_todos()
    print(f"✅ Total suplementos en BD: {len(todos)}")
    for s in todos:
        print(f"   💊 [{s.codigo}] {s.nombre} - Stock: {s.stock} - Precio USD: ${s.precioUSD}")

if __name__ == "__main__":
    test_crud_suplemento()
