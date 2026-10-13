#!/usr/bin/env python3
"""PowerFit - Utilidad CLI para Reiniciar y Poblar la Base de Datos SQLite."""
import sys
from pathlib import Path

# Agregar directorio raíz al sys.path
RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from src.dao.conexion import ConexionDB
from src.dao.trabajador_dao import TrabajadorDAO
from src.dao.socio_dao import SocioDAO
from src.dao.clase_dao import ClaseDAO
from src.dao.suplemento_dao import SuplementoDAO


def reset_database():
    print("=" * 65)
    print(" 🏋️ POWERFIT GYM - RESTABLECIMIENTO DE BASE DE DATOS SQLITE")
    print("=" * 65)
    print("⏳ Limpiando tablas y reconstruyendo esquema...")

    ConexionDB.reiniciar_base_datos(con_semilla=True)

    print("✅ Esquema recreado exitosamente.")
    print("🌱 Poblado de datos semilla completado:")

    # Mostrar resumen
    trab_dao = TrabajadorDAO()
    socio_dao = SocioDAO()
    clase_dao = ClaseDAO()
    sup_dao = SuplementoDAO()

    trabajadores = trab_dao.obtener_todos()
    print(f"\n👤 PERSONAL REGISTRADO ({len(trabajadores)} usuarios - Hashes Argon2id protegidos):")
    demo_passwords = {"admin": "admin123", "recepcion": "rec123", "instructor": "ins123"}
    for t in trabajadores:
        clave_demo = demo_passwords.get(t.usuario, "••••••••")
        print(f"   • [{t.getRol():<13}] {t.getNombres()} {t.getApellidoPaterno()} -> Usuario: '{t.usuario}' (Clave Demo: '{clave_demo}')")

    socios = socio_dao.obtener_todos()
    print(f"\n🏷️  SOCIOS DE PRUEBA ({len(socios)} socios con estados para torniquete):")
    for s in socios:
        icono = "🟢" if s.estado_membresia == "Al Día" else ("🔴" if s.estado_membresia == "Vencida" else "⚪")
        print(f"   • {icono} [{s.estado_membresia:<8}] {s.getNombres()} {s.getApellidoPaterno()} (RUT: {s.rut}) -> Vence: {s.fechaVencimientoMembresia}")

    clases = clase_dao.obtener_todos()
    print(f"\n🏋️ CLASES DIRIGIDAS ({len(clases)} disciplinas con salas y cupos):")
    for c in clases:
        icono = c.obtener_icono_disciplina()
        print(f"   • {icono} {c.nombre:<20} | Cupo: {c.cupoMaximo} | Sala: {c.sala}")

    suplementos = sup_dao.obtener_todos()
    print(f"\n💊 CATÁLOGO DE SUPLEMENTOS ({len(suplementos)} productos en stock):")
    for sup in suplementos:
        print(f"   • [{sup.codigo:>2}] {sup.nombre:<38} | ${sup.precioUSD:>6.2f} USD | Stock: {sup.stock}")

    print("\n" + "=" * 65)
    print("✨ ¡Base de datos lista para pruebas y presentaciones en vivo!")
    print("=" * 65)


if __name__ == "__main__":
    reset_database()
