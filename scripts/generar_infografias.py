"""Script ultra-diseñado para generar infografías HD profesionales del proyecto PowerFit."""
import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patheffects import withStroke

# Crear directorio docs si no existe
os.makedirs("docs", exist_ok=True)

# Estilos globales
FONT_FAMILY = "sans-serif"
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']

# -----------------------------------------------------------------------------
# 1. INFOGRAFÍA 1: ROADMAP POO BACKEND (docs/roadmap_powerfit.jpg)
# -----------------------------------------------------------------------------
def generar_roadmap_backend():
    fig, ax = plt.subplots(figsize=(14, 8), dpi=300)
    fig.patch.set_facecolor("#0B0F19")
    ax.set_facecolor("#0B0F19")
    ax.axis("off")

    # Header con sombra y gradiente visual
    t1 = plt.text(0.5, 0.93, "POWERFIT - ROADMAP DE DESARROLLO POO BACKEND", 
                 fontsize=18, fontweight="bold", color="#38BDF8", ha="center")
    t1.set_path_effects([withStroke(linewidth=2, foreground="#0284C7")])
    
    plt.text(0.5, 0.88, "Arquitectura Integral 20/10: Clases Abstractas, Polimorfismo, Dominio & Validaciones", 
             fontsize=11, color="#94A3B8", ha="center")

    fases = [
        {"fase": "FASE 1", "titulo": "Fundamentos & Modelos Base", "estado": "[ COMPLETADA ]", 
         "color": "#10B981", "desc": "Clase Abstracta Persona (Validacion RUT Modulo 11), Direccion y 346 Comunas INE Chile."},
        {"fase": "FASE 2", "titulo": "Jerarquia de Usuarios & Roles RBAC", "estado": "[ COMPLETADA ]", 
         "color": "#10B981", "desc": "Socio (permitirIngreso), Trabajador (tienePermiso), Instructor, Recepcionista y Administrador."},
        {"fase": "FASE 3", "titulo": "Motor de Clases & Membresias", "estado": "[ COMPLETADA ]", 
         "color": "#10B981", "desc": "Clase base, ClaseDirigida polimorfica (Yoga, Spinning, Crossfit), InscripcionMensual y DetalleInscripcion."},
        {"fase": "FASE 4", "titulo": "Punto de Venta & API Dolar", "estado": "[ COMPLETADA ]", 
         "color": "#10B981", "desc": "Suplemento (hayStock/descontarStock), IndicadorDolar (mindicador.cl), Venta y DetalleVenta en CLP."},
        {"fase": "FASE 5", "titulo": "Simulador Torniquete & QA Final", "estado": "[ COMPLETADA ]", 
         "color": "#10B981", "desc": "Control de Porteria, Popups Alerta (QMessageBox.critical), Gestion Personal Admin y suite pytest."}
    ]

    y_pos = 0.77
    for item in fases:
        # Sombra del bloque
        shadow = patches.FancyBboxPatch((0.062, y_pos - 0.082), 0.876, 0.095, 
                                       boxstyle="round,pad=0.015", 
                                       linewidth=0, facecolor="#030712", alpha=0.5)
        ax.add_patch(shadow)

        # Bloque de la fase
        rect = patches.FancyBboxPatch((0.06, y_pos - 0.08), 0.88, 0.095, 
                                     boxstyle="round,pad=0.015", 
                                     linewidth=2, edgecolor=item["color"], facecolor="#1E293B")
        ax.add_patch(rect)

        # Indicador de estado a la izquierda
        indicator = patches.Rectangle((0.06, y_pos - 0.08), 0.015, 0.095, color=item["color"])
        ax.add_patch(indicator)

        # Texto Fase & Titulo
        plt.text(0.09, y_pos - 0.03, f"{item['fase']}: {item['titulo']}", 
                 fontsize=12, fontweight="bold", color="#F8FAFC", va="center")
        
        # Estado
        plt.text(0.92, y_pos - 0.03, item['estado'], 
                 fontsize=11, fontweight="bold", color=item["color"], ha="right", va="center")
        
        # Descripción
        plt.text(0.09, y_pos - 0.06, item['desc'], 
                 fontsize=9.5, color="#CBD5E1", va="center")

        y_pos -= 0.125

    # Footer
    plt.text(0.5, 0.03, "PowerFit Gym System - Universidad Inacap 2026 | Arquitectura de Software POO", 
             fontsize=9, color="#64748B", ha="center")

    plt.tight_layout()
    plt.savefig("docs/roadmap_powerfit.jpg", bbox_inches="tight", facecolor=fig.get_facecolor(), dpi=300)
    plt.close()
    print("✅ Generado docs/roadmap_powerfit.jpg")


# -----------------------------------------------------------------------------
# 2. INFOGRAFÍA 2: ROADMAP GUI PYSIDE6 (docs/roadmap_gui_powerfit.jpg)
# -----------------------------------------------------------------------------
def generar_roadmap_gui():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#0F172A")
    ax.axis("off")

    t1 = plt.text(0.5, 0.94, "POWERFIT - ROADMAP DE INTERFAZ GRAFICA (PySide6 GUI)", 
                 fontsize=18, fontweight="bold", color="#F97316", ha="center")
    t1.set_path_effects([withStroke(linewidth=2, foreground="#EA580C")])

    plt.text(0.5, 0.89, "Progreso en Vivo de los Hitos Visuales, QStackedWidget & Dual-Theme (Dark/Light)", 
             fontsize=11, color="#94A3B8", ha="center")

    hitos = [
        {"hito": "HITO 1", "titulo": "Marco Principal QMainWindow & Layouts", "estado": "[ COMPLETADO ]", 
         "desc": "Ventana 980x700, barra superior navegable, conmutador Dual-Theme y QStackedWidget multitarea."},
        {"hito": "HITO 2", "titulo": "Modulo de Gestion de Socios & Comunas", "estado": "[ COMPLETADO ]", 
         "desc": "Formulario QFormLayout, 346 comunas de Chile (INE A-Z), Direccion completa y alertas de validacion."},
        {"hito": "HITO 3", "titulo": "Mapa Visual de Salas & Clases Dirigidas", "estado": "[ COMPLETADO ]", 
         "desc": "Formulario Yoga/Spinning/Crossfit, control de cupos y Mapa Interactivo de Puestos (Mats, Bicis, Estaciones)."},
        {"hito": "HITO 4", "titulo": "Punto de Venta & API Dolar en Vivo", "estado": "[ COMPLETADO ]", 
         "desc": "Catalogo de suplementos, consulta en tiempo real a mindicador.cl y calculo transaccional Venta/DetalleVenta."},
        {"hito": "HITO 5", "titulo": "Simulador de Torniquete & Popups Alerta", "estado": "[ COMPLETADO ]", 
         "desc": "Control de Porteria en tiempo real con invocacion socio.permitirIngreso() y Popups de Alerta Flotante."},
        {"hito": "HITO 6", "titulo": "Perfilamiento, Roles & Alta de Personal Admin", "estado": "[ COMPLETADO ]", 
         "desc": "Autenticacion RBAC (Admin/Recepcion/Instructor), alta de trabajadores y cobro/cancelacion de membresias."}
    ]

    y_pos = 0.80
    for item in hitos:
        shadow = patches.FancyBboxPatch((0.062, y_pos - 0.072), 0.876, 0.085, 
                                       boxstyle="round,pad=0.015", 
                                       linewidth=0, facecolor="#020617", alpha=0.5)
        ax.add_patch(shadow)

        rect = patches.FancyBboxPatch((0.06, y_pos - 0.07), 0.88, 0.085, 
                                     boxstyle="round,pad=0.015", 
                                     linewidth=2, edgecolor="#F97316", facecolor="#1E293B")
        ax.add_patch(rect)

        indicator = patches.Rectangle((0.06, y_pos - 0.07), 0.015, 0.085, color="#F97316")
        ax.add_patch(indicator)

        plt.text(0.09, y_pos - 0.025, f"{item['hito']}: {item['titulo']}", 
                 fontsize=11.5, fontweight="bold", color="#F8FAFC", va="center")
        plt.text(0.92, y_pos - 0.025, item['estado'], 
                 fontsize=11, fontweight="bold", color="#34D399", ha="right", va="center")
        
        plt.text(0.09, y_pos - 0.052, item['desc'], 
                 fontsize=9.5, color="#CBD5E1", va="center")

        y_pos -= 0.11

    plt.text(0.5, 0.03, "PowerFit PySide6 GUI - Estado: Todos los Hitos Visuales e Interacciones COMPLETADOS (100%)", 
             fontsize=9, color="#64748B", ha="center")

    plt.tight_layout()
    plt.savefig("docs/roadmap_gui_powerfit.jpg", bbox_inches="tight", facecolor=fig.get_facecolor(), dpi=300)
    plt.close()
    print("✅ Generado docs/roadmap_gui_powerfit.jpg")


# -----------------------------------------------------------------------------
# 3. INFOGRAFÍA 3: MATRIZ RBAC & ROLES (docs/powerfit_rbac_profiles.jpg)
# -----------------------------------------------------------------------------
def generar_infografia_rbac():
    fig, ax = plt.subplots(figsize=(14, 8.5), dpi=300)
    fig.patch.set_facecolor("#0F172A")
    ax.set_facecolor("#0F172A")
    ax.axis("off")

    t1 = plt.text(0.5, 0.94, "POWERFIT - MATRIZ DE PERFILAMIENTO Y ROLES RBAC", 
                 fontsize=18, fontweight="bold", color="#38BDF8", ha="center")
    t1.set_path_effects([withStroke(linewidth=2, foreground="#0284C7")])

    plt.text(0.5, 0.89, "Control de Acceso Basado en Roles (Role-Based Access Control) en GUI & Modelos Backend", 
             fontsize=11, color="#94A3B8", ha="center")

    roles = [
        {"rol": "ADMINISTRADOR", "user": "admin / admin123", "color": "#EF4444", 
         "permisos": ["+ Acceso Total a Gestion de Socios", "+ Acceso Total a Clases Dirigidas", "+ Acceso a Punto de Venta & API Dolar", "+ Alta de Personal (crearTrabajador)", "+ Reposicion de Stock (reponerStock)"]},
        {"rol": "RECEPCIONISTA", "user": "recepcion / rec123", "color": "#F59E0B", 
         "permisos": ["+ Acceso a Registro de Socios", "+ Cobro de Cuota (cobrarMensualidad)", "+ Cancelar / Desactivar Membresia", "+ Acceso a Punto de Venta & Dolar", "- Oculto: Modulo de Personal Admin"]},
        {"rol": "INSTRUCTOR", "user": "instructor / ins123", "color": "#3B82F6", 
         "permisos": ["+ Acceso Total a Clases Dirigidas", "+ Dictar Clase (dictarClase)", "+ Tomar Asistencia (marcarAsistencia)", "- Oculto: Registro de Socios", "- Oculto: Punto de Venta & Admin"]}
    ]

    x_pos = [0.05, 0.36, 0.67]
    width = 0.28

    for i, item in enumerate(roles):
        x = x_pos[i]
        
        shadow = patches.FancyBboxPatch((x + 0.005, 0.13), width, 0.68, 
                                       boxstyle="round,pad=0.02", 
                                       linewidth=0, facecolor="#020617", alpha=0.5)
        ax.add_patch(shadow)

        rect = patches.FancyBboxPatch((x, 0.14), width, 0.68, 
                                     boxstyle="round,pad=0.02", 
                                     linewidth=2.5, edgecolor=item["color"], facecolor="#1E293B")
        ax.add_patch(rect)

        # Encabezado Rol
        plt.text(x + width/2, 0.76, item["rol"], 
                 fontsize=13, fontweight="bold", color=item["color"], ha="center", va="center")
        plt.text(x + width/2, 0.71, f"Credencial: {item['user']}", 
                 fontsize=9.5, color="#CBD5E1", ha="center", va="center")

        ax.plot([x + 0.02, x + width - 0.02], [0.67, 0.67], color="#334155", lw=1.5)

        y_perm = 0.61
        for perm in item["permisos"]:
            color_text = "#4ADE80" if perm.startswith("+") else "#F87171"
            prefix = "[OK] " if perm.startswith("+") else "[NO] "
            clean_perm = perm[2:]
            plt.text(x + 0.02, y_perm, f"{prefix}{clean_perm}", fontsize=8.8, fontweight="bold", color=color_text, va="center")
            y_perm -= 0.085

    plt.text(0.5, 0.03, "Seguridad RBAC PowerFit - Encapsulamiento POO con @property & Autenticacion de Credenciales", 
             fontsize=9, color="#64748B", ha="center")

    plt.tight_layout()
    plt.savefig("docs/powerfit_rbac_profiles.jpg", bbox_inches="tight", facecolor=fig.get_facecolor(), dpi=300)
    plt.close()
    print("✅ Generado docs/powerfit_rbac_profiles.jpg")


# -----------------------------------------------------------------------------
# 4. INFOGRAFÍA 4: ROADMAP SUMATIVA 2 (docs/roadmap_sumativa2.jpg)
# -----------------------------------------------------------------------------
def generar_roadmap_sumativa2():
    fig, ax = plt.subplots(figsize=(14, 9), dpi=300)
    fig.patch.set_facecolor("#0B0F19")
    ax.set_facecolor("#0B0F19")
    ax.axis("off")

    t1 = plt.text(0.5, 0.94, "POWERFIT - ROADMAP SUMATIVA 2: REQUISITOS DE NEGOCIO", 
                 fontsize=18, fontweight="bold", color="#10B981", ha="center")
    t1.set_path_effects([withStroke(linewidth=2, foreground="#059669")])

    plt.text(0.5, 0.89, "Estado de Avance de los Modulos Operacionales y Evaluacion Academica POO", 
             fontsize=11, color="#94A3B8", ha="center")

    modulos = [
        {
            "num": "MODULO 1", "titulo": "Cobro de Cuota & Vigencia Membresia", "estado": "[ COMPLETADA ]",
            "color": "#10B981", "actor": "Recepcionista",
            "desc": "Ejecutar cobrarMensualidad() extendiendo fecha +30d. Gestion de estados 'Al Dia', 'Impago' y 'Cancelado'."
        },
        {
            "num": "MODULO 2", "titulo": "Simulador de Torniquete (Control Porteria)", "estado": "[ COMPLETADA ]",
            "color": "#10B981", "actor": "Control Porteria",
            "desc": "Validar RUT con permitirIngreso(). Alerta de pase verde o Popups de Alerta Flotante (QMessageBox.critical)."
        },
        {
            "num": "MODULO 3", "titulo": "Control de Stock e Inventario POS", "estado": "[ COMPLETADA ]",
            "color": "#10B981", "actor": "Punto de Venta",
            "desc": "Verificar hayStock() antes de cobrar, descuento de inventario Suplemento y Reposicion Admin (reponerStock)."
        },
        {
            "num": "MODULO 4", "titulo": "Registro de Asistencia a Clases", "estado": "[ COMPLETADA ]",
            "color": "#10B981", "actor": "Instructor",
            "desc": "Ejecutar marcarAsistencia(socio, clase) e inscribir_socio() desde el mapa interactivo de puestos de sala."
        },
        {
            "num": "MODULO 5", "titulo": "Agrupacion Transaccional de Reservas", "estado": "[ COMPLETADA ]",
            "color": "#10B981", "actor": "Inscripcion Mensual",
            "desc": "Objetos InscripcionMensual con DetalleInscripcion (Composicion 1..*) y Venta con DetalleVenta."
        },
        {
            "num": "MODULO 6", "titulo": "Persistencia de Datos SQLite & DAO", "estado": "[ PENDIENTE ]",
            "color": "#64748B", "actor": "Base de Datos Local",
            "desc": "Modelado de tablas relacionales en sqlite3 y patron de acceso DAO (Data Access Object)."
        }
    ]

    y_pos = 0.80
    for item in modulos:
        shadow = patches.FancyBboxPatch((0.062, y_pos - 0.072), 0.876, 0.085, 
                                       boxstyle="round,pad=0.015", 
                                       linewidth=0, facecolor="#030712", alpha=0.5)
        ax.add_patch(shadow)

        rect = patches.FancyBboxPatch((0.06, y_pos - 0.07), 0.88, 0.085, 
                                     boxstyle="round,pad=0.015", 
                                     linewidth=2, edgecolor=item["color"], facecolor="#1E293B")
        ax.add_patch(rect)

        indicator = patches.Rectangle((0.06, y_pos - 0.07), 0.015, 0.085, color=item["color"])
        ax.add_patch(indicator)

        plt.text(0.09, y_pos - 0.025, f"{item['num']}: {item['titulo']}", 
                 fontsize=11.5, fontweight="bold", color="#F8FAFC", va="center")
        plt.text(0.55, y_pos - 0.025, f"Actor: {item['actor']}", 
                 fontsize=10, fontweight="bold", color="#38BDF8", va="center")
        plt.text(0.92, y_pos - 0.025, item['estado'], 
                 fontsize=10.5, fontweight="bold", color=item["color"], ha="right", va="center")
        
        plt.text(0.09, y_pos - 0.052, item['desc'], 
                 fontsize=9.5, color="#CBD5E1", va="center")

        y_pos -= 0.11

    plt.text(0.5, 0.03, "PowerFit Gym - Roadmap Tecnico Sumativa 2 | 5 de 6 Modulos Completados al 100%", 
             fontsize=9, color="#64748B", ha="center")

    plt.tight_layout()
    plt.savefig("docs/roadmap_sumativa2.jpg", bbox_inches="tight", facecolor=fig.get_facecolor(), dpi=300)
    plt.close()
    print("✅ Generado docs/roadmap_sumativa2.jpg")


if __name__ == "__main__":
    generar_roadmap_backend()
    generar_roadmap_gui()
    generar_infografia_rbac()
    generar_roadmap_sumativa2()
    print("🚀 ¡Todas las infografías del proyecto se actualizaron exitosamente a diseño HD profesional!")
