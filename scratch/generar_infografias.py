"""Script para generar las 3 infografías del proyecto PowerFit con estado actualizado en vivo."""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Crear directorio docs si no existe
os.makedirs("docs", exist_ok=True)

# -----------------------------------------------------------------------------
# 1. INFOGRAFÍA 1: ROADMAP POO BACKEND (docs/roadmap_powerfit.jpg)
# -----------------------------------------------------------------------------
def generar_roadmap_backend():
    fig, ax = plt.subplots(figsize=(12, 7), dpi=200)
    fig.patch.set_facecolor("#1A252F")
    ax.set_facecolor("#1A252F")
    ax.axis("off")

    # Título Principal
    plt.text(0.5, 0.92, "🏋️ PowerFit - Roadmap de Desarrollo Backend POO", 
             fontsize=18, fontweight="bold", color="#ECF0F1", ha="center")
    plt.text(0.5, 0.86, "Arquitectura de Clases UML, Herencia, Polimorfismo & Validaciones Dominio", 
             fontsize=11, color="#BDC3C7", ha="center")

    fases = [
        {"fase": "Fase 1", "titulo": "Fundamentos & Modelos Base", "estado": "🟢 COMPLETADA", 
         "color": "#27AE60", "desc": "Clase Persona (RUT Módulo 11), Direccion y Comunas INE Chile."},
        {"fase": "Fase 2", "titulo": "Jerarquía de Usuarios & Roles", "estado": "🟢 COMPLETADA", 
         "color": "#27AE60", "desc": "Socio, Trabajador, Instructor, Recepcionista, Administrador (ABC/@property)."},
        {"fase": "Fase 3", "titulo": "Motor de Clases & Membresías", "estado": "⚪ PRÓXIMA", 
         "color": "#3498DB", "desc": "Yoga, Spinning, Crossfit, Cupos, Inscripciones y Membresias."},
        {"fase": "Fase 4", "titulo": "Punto de Venta & API Dólar", "estado": "⚪ PENDIENTE", 
         "color": "#E67E22", "desc": "Suplemento, Stock, IndicadorDolar (CLP) y DetalleVenta."},
        {"fase": "Fase 5", "titulo": "Consola CLI & QA Final", "estado": "⚪ PENDIENTE", 
         "color": "#95A5A6", "desc": "Menú interactivo CLI por rol, suite pytest e integración final."}
    ]

    y_pos = 0.72
    for item in fases:
        # Bloque de la fase
        rect = patches.FancyBboxPatch((0.08, y_pos - 0.08), 0.84, 0.1, 
                                     boxstyle="round,pad=0.02", 
                                     linewidth=2, edgecolor=item["color"], facecolor="#2C3E50")
        ax.add_patch(rect)

        # Texto Fase & Estado
        plt.text(0.11, y_pos - 0.02, f"{item['fase']}: {item['titulo']}", 
                 fontsize=13, fontweight="bold", color="#FFFFFF", va="center")
        plt.text(0.89, y_pos - 0.02, item['estado'], 
                 fontsize=11, fontweight="bold", color=item["color"], ha="right", va="center")
        
        # Descripción
        plt.text(0.11, y_pos - 0.055, item['desc'], 
                 fontsize=10, color="#BDC3C7", va="center")

        y_pos -= 0.13

    # Pie de página
    plt.text(0.5, 0.03, "PowerFit Gym System - Universidad Inacap | Versión 0.4.0 Live", 
             fontsize=9, color="#7F8C8D", ha="center")

    plt.tight_layout()
    plt.savefig("docs/roadmap_powerfit.jpg", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print("✅ Generado docs/roadmap_powerfit.jpg")


# -----------------------------------------------------------------------------
# 2. INFOGRAFÍA 2: ROADMAP GUI PYSIDE6 (docs/roadmap_gui_powerfit.jpg)
# -----------------------------------------------------------------------------
def generar_roadmap_gui():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=200)
    fig.patch.set_facecolor("#111827")
    ax.set_facecolor("#111827")
    ax.axis("off")

    plt.text(0.5, 0.93, "🎨 PowerFit - Roadmap de Interfaz Gráfica (PySide6 GUI)", 
             fontsize=18, fontweight="bold", color="#F9FAFB", ha="center")
    plt.text(0.5, 0.88, "Progreso en Vivo de los Hitos Visuales & Módulos QStackedWidget", 
             fontsize=11, color="#9CA3AF", ha="center")

    hitos = [
        {"hito": "Hito 1", "titulo": "Marco Principal QMainWindow", "estado": "🟢 COMPLETADA", 
         "desc": "Ventana 850x650, layouts horizontales/verticales, estilos CSS y navegabilidad QStackedWidget."},
        {"hito": "Hito 2", "titulo": "Módulo de Gestión de Socios", "estado": "🟢 COMPLETADA", 
         "desc": "Formulario QFormLayout, combobox de 346 comunas de Chile ordenadas A-Z y alertas QMessageBox."},
        {"hito": "Hito 3", "titulo": "Módulo de Clases Dirigidas", "estado": "🟢 COMPLETADA", 
         "desc": "Formulario para Yoga, Spinning y Crossfit, control de cupos máximos y duraciones."},
        {"hito": "Hito 4", "titulo": "Punto de Venta & API Dólar", "estado": "🟢 COMPLETADA", 
         "desc": "Catálogo de suplementos y consulta en vivo a mindicador.cl autocompletando tasa CLP."},
        {"hito": "Hito 5", "titulo": "Tablas QTableWidget en Vivo", "estado": "🟢 COMPLETADA", 
         "desc": "Tablas dinámicas multitarea insertando registros en tiempo real en Socios, Clases y Ventas."},
        {"hito": "Hito 6", "titulo": "Perfilamiento, Roles & Login RBAC", "estado": "🟢 COMPLETADA", 
         "desc": "Tarjeta de Login, autenticación de credenciales y navegación filtrada por rol (Admin/Recepción/Instructor)."}
    ]

    y_pos = 0.77
    for item in hitos:
        rect = patches.FancyBboxPatch((0.08, y_pos - 0.075), 0.84, 0.09, 
                                     boxstyle="round,pad=0.015", 
                                     linewidth=2, edgecolor="#10B981", facecolor="#1F2937")
        ax.add_patch(rect)

        plt.text(0.11, y_pos - 0.025, f"{item['hito']}: {item['titulo']}", 
                 fontsize=12, fontweight="bold", color="#FFFFFF", va="center")
        plt.text(0.89, y_pos - 0.025, item['estado'], 
                 fontsize=11, fontweight="bold", color="#10B981", ha="right", va="center")
        
        plt.text(0.11, y_pos - 0.055, item['desc'], 
                 fontsize=9.5, color="#D1D5DB", va="center")

        y_pos -= 0.115

    plt.text(0.5, 0.03, "PowerFit PySide6 GUI Roadmap - Estado: Todos los Hitos Completados (100%)", 
             fontsize=9, color="#6B7280", ha="center")

    plt.tight_layout()
    plt.savefig("docs/roadmap_gui_powerfit.jpg", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print("✅ Generado docs/roadmap_gui_powerfit.jpg")


# -----------------------------------------------------------------------------
# 3. INFOGRAFÍA 3: MATRIZ RBAC & ROLES (docs/powerfit_rbac_profiles.jpg)
# -----------------------------------------------------------------------------
def generar_infografia_rbac():
    fig, ax = plt.subplots(figsize=(12, 8), dpi=200)
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#0F172A")
    ax.axis("off")

    plt.text(0.5, 0.93, "🔐 PowerFit - Matriz de Perfilamiento y Roles RBAC", 
             fontsize=18, fontweight="bold", color="#F8FAFC", ha="center")
    plt.text(0.5, 0.88, "Control de Acceso Basado en Roles (Role-Based Access Control) en GUI & API", 
             fontsize=11, color="#94A3B8", ha="center")

    roles = [
        {"rol": "👑 ADMINISTRADOR", "user": "admin / admin123", "color": "#EF4444", 
         "permisos": ["✅ Acceso Total a Gestión de Socios", "✅ Acceso Total a Clases Dirigidas", "✅ Acceso a Punto de Venta & API Dólar", "✅ Gestión de Usuarios & Configuración"]},
        {"rol": "🛎️ RECEPCIONISTA", "user": "recepcion / rec123", "color": "#F59E0B", 
         "permisos": ["✅ Acceso a Registro de Socios", "❌ Oculto: Clases Dirigidas (Restringido)", "✅ Acceso a Punto de Venta & Cobranza", "❌ Oculto: Configuración Admin"]},
        {"rol": "🏋️ INSTRUCTOR", "user": "instructor / ins123", "color": "#3B82F6", 
         "permisos": ["❌ Oculto: Registro de Socios (Restringido)", "✅ Acceso Total a Clases Dirigidas", "❌ Oculto: Punto de Venta (Restringido)", "❌ Oculto: Configuración Admin"]}
    ]

    x_pos = [0.06, 0.37, 0.68]
    width = 0.26

    for i, item in enumerate(roles):
        x = x_pos[i]
        rect = patches.FancyBboxPatch((x, 0.15), width, 0.65, 
                                     boxstyle="round,pad=0.02", 
                                     linewidth=2.5, edgecolor=item["color"], facecolor="#1E293B")
        ax.add_patch(rect)

        # Encabezado Rol
        plt.text(x + width/2, 0.74, item["rol"], 
                 fontsize=12, fontweight="bold", color=item["color"], ha="center", va="center")
        plt.text(x + width/2, 0.69, f"Credencial: {item['user']}", 
                 fontsize=9, color="#CBD5E1", ha="center", va="center")

        # Línea separadora
        ax.plot([x + 0.02, x + width - 0.02], [0.65, 0.65], color="#334155", lw=1.5)

        # Lista de Permisos
        y_perm = 0.59
        for perm in item["permisos"]:
            color_text = "#4ADE80" if perm.startswith("✅") else "#F87171"
            plt.text(x + 0.02, y_perm, perm, fontsize=8.5, color=color_text, va="center")
            y_perm -= 0.09

    plt.text(0.5, 0.04, "Seguridad RBAC PowerFit - Encapsulamiento POO con @property & Autenticación de Credenciales", 
             fontsize=9, color="#64748B", ha="center")

    plt.tight_layout()
    plt.savefig("docs/powerfit_rbac_profiles.jpg", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print("✅ Generado docs/powerfit_rbac_profiles.jpg")


# -----------------------------------------------------------------------------
# 4. INFOGRAFÍA 4: ROADMAP SUMATIVA 2 & REQUISITOS DEL PROFESOR (docs/roadmap_sumativa2.jpg)
# -----------------------------------------------------------------------------
def generar_roadmap_sumativa2():
    fig, ax = plt.subplots(figsize=(12, 8.5), dpi=200)
    fig.patch.set_facecolor("#0D1117")
    ax.set_facecolor("#0D1117")
    ax.axis("off")

    plt.text(0.5, 0.94, "📋 PowerFit - Roadmap Sumativa 2: Requisitos de Negocio & Faltantes", 
             fontsize=17, fontweight="bold", color="#F0F6FC", ha="center")
    plt.text(0.5, 0.89, "Plan de Trabajo alineado al Enunciado Oficial & Retroalimentación del Docente", 
             fontsize=11, color="#8B949E", ha="center")

    modulos = [
        {
            "num": "Módulo 1", "titulo": "Cobro de Cuota & Vigencia Membresía", "estado": "🟡 EN DESARROLLO",
            "color": "#F59E0B", "actor": "🛎️ Recepcionista",
            "desc": "Ejecutar cobrarMensualidad() extendiendo fecha +30 días. Estado visual 'Al Día' / 'Vencido'."
        },
        {
            "num": "Módulo 2", "titulo": "Simulador de Torniquete (Control de Acceso)", "estado": "⚪ PENDIENTE",
            "color": "#3B82F6", "actor": "🚪 Control Portería",
            "desc": "Validar RUT con permitirIngreso(). Mostrar alerta verde (Pasa) o bloqueo rojo (Membresía Vencida)."
        },
        {
            "num": "Módulo 3", "titulo": "Control de Stock e Inventario en POS", "estado": "🟡 EN DESARROLLO",
            "color": "#F59E0B", "actor": "🛒 Punto de Venta",
            "desc": "Verificar hayStock() antes de cobrar y descontar inventario físico de Suplemento tras cada venta."
        },
        {
            "num": "Módulo 4", "titulo": "Registro de Asistencia a Clases", "estado": "⚪ PENDIENTE",
            "color": "#8B5CF6", "actor": "🏋️ Instructor",
            "desc": "Ejecutar marcarAsistencia(socio, clase) desde el mapa interactivo de puestos de la sala."
        },
        {
            "num": "Módulo 5", "titulo": "Agrupación Transaccional de Reservas", "estado": "🟢 MODELADO",
            "color": "#10B981", "actor": "✍️ Inscripción Mensual",
            "desc": "Objeto InscripcionMensual conteniendo múltiples DetalleInscripcion (Composición 1 a 1..*)."
        },
        {
            "num": "Módulo 6", "titulo": "Persistencia de Datos con SQLite", "estado": "⚪ FASE FINAL",
            "color": "#6B7280", "actor": "💾 Base de Datos Local",
            "desc": "Tablas relacionales en sqlite3: socios, membresias, clases, inscripciones y ventas."
        }
    ]

    y_pos = 0.80
    for item in modulos:
        rect = patches.FancyBboxPatch((0.07, y_pos - 0.08), 0.86, 0.095, 
                                     boxstyle="round,pad=0.015", 
                                     linewidth=2, edgecolor=item["color"], facecolor="#161B22")
        ax.add_patch(rect)

        # Encabezado
        plt.text(0.10, y_pos - 0.025, f"{item['num']}: {item['titulo']}", 
                 fontsize=11.5, fontweight="bold", color="#FFFFFF", va="center")
        plt.text(0.55, y_pos - 0.025, item["actor"], 
                 fontsize=10, fontweight="bold", color="#93C5FD", va="center")
        plt.text(0.90, y_pos - 0.025, item['estado'], 
                 fontsize=10.5, fontweight="bold", color=item["color"], ha="right", va="center")
        
        # Descripción
        plt.text(0.10, y_pos - 0.055, item['desc'], 
                 fontsize=9.5, color="#C9D1D9", va="center")

        y_pos -= 0.115

    plt.text(0.5, 0.03, "PowerFit Gym - Roadmap Técnico Sumativa 2 | POO Seguro INACAP", 
             fontsize=9, color="#8B949E", ha="center")

    plt.tight_layout()
    plt.savefig("docs/roadmap_sumativa2.jpg", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print("✅ Generado docs/roadmap_sumativa2.jpg")


if __name__ == "__main__":
    generar_roadmap_backend()
    generar_roadmap_gui()
    generar_infografia_rbac()
    generar_roadmap_sumativa2()
    print("🚀 ¡Todas las infografías del proyecto se actualizaron exitosamente!")
