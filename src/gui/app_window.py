"""PowerFit - Punto de entrada principal con Autenticación y Control de Acceso por Roles (RBAC - Hito 6)."""
import os
import sys
import json
import urllib.request
import uuid

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
    QHBoxLayout,
    QStackedWidget,
    QFormLayout,
    QComboBox,
    QTableWidget,
    QTableWidgetItem,
    QGridLayout,
    QGroupBox,
)
from PySide6.QtCore import Qt

from src.models import (
    Persona,
    Direccion,
    Comuna,
    cargar_comunas_ine,
    Trabajador,
    Administrador,
    Instructor,
    Recepcionista,
    Socio,
    ClaseSpinning,
    ClaseYoga,
    ClaseCrossfit,
    Suplemento,
    IndicadorDolar,
    Venta,
    DetalleVenta,
    InscripcionMensual,
)


class VentanaPrincipalPowerFit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PowerFit - Sistema de Gestión de Gimnasio")
        self.resize(980, 700)
        
        # Estado de Tema Visual ("dark" | "light")
        self.modo_oscuro_activo = True

        # Hojas de estilo QSS para Modo Oscuro y Modo Claro
        from src.gui.styles import QSS_MODO_OSCURO, QSS_MODO_CLARO
        self.QSS_MODO_OSCURO = QSS_MODO_OSCURO
        self.QSS_MODO_CLARO = QSS_MODO_CLARO

        self.setStyleSheet(self.QSS_MODO_OSCURO)

        # Usuario autenticado actualmente
        self.usuario_actual = None

        # Base de datos simulada de usuarios del sistema (RBAC)
        self.usuarios_sistema = {
            "admin": Administrador(
                nivelAcceso="Total/SuperUser",
                idTrabajador=1,
                usuario="admin",
                passHash="admin123",
                rut="11.111.111-1",
                nombres="Administrador",
                apellidoPaterno="General",
                apellidoMaterno="PowerFit",
                telefono="912345678",
                correoElectronico="admin@powerfit.cl",
            ),
            "recepcion": Recepcionista(
                turno="Mañana",
                idTrabajador=2,
                usuario="recepcion",
                passHash="rec123",
                rut="22.222.222-2",
                nombres="María Paz",
                apellidoPaterno="Gómez",
                apellidoMaterno="Soto",
                telefono="987654321",
                correoElectronico="recepcion@powerfit.cl",
            ),
            "instructor": Instructor(
                especialidad="Crossfit & Spinning",
                idTrabajador=3,
                usuario="instructor",
                passHash="ins123",
                rut="33.333.333-3",
                nombres="Juan Pablo",
                apellidoPaterno="Pérez",
                apellidoMaterno="Vargas",
                telefono="955554444",
                correoElectronico="instructor@powerfit.cl",
            ),
        }

        # Almacenamiento en memoria de objetos del dominio POO
        self.socios_registrados = []
        self.clases_registradas = {}  # dict: {nombre_clase: obj ClaseDirigida}
        self.clase_seleccionada_actual = None

        # Layout Principal
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_principal = QVBoxLayout(self.widget_central)

        # 1. Barra superior de navegación (inicialmente oculta antes del Login)
        self.barras_navegacion = QWidget()
        self.barras_navegacion.setObjectName("barras_navegacion")
        self.barras_navegacion.setStyleSheet("background-color: #1E293B; border-radius: 8px; padding: 4px;")
        layout_nav = QHBoxLayout(self.barras_navegacion)

        self.lbl_usuario_status = QLabel("👤 No autenticado")
        self.lbl_usuario_status.setStyleSheet("font-weight: bold; color: #38BDF8; font-size: 13px;")

        self.btn_toggle_tema = QPushButton("☀️ Modo Claro")
        self.btn_toggle_tema.setStyleSheet("background-color: #0284C7; color: white; padding: 6px 12px; font-weight: bold; border-radius: 6px;")
        self.btn_toggle_tema.clicked.connect(self.alternar_tema)

        self.btn_socios = QPushButton("👤 Gestión de Socios")
        self.btn_clases = QPushButton("🏋️ Clases Dirigidas")
        self.btn_ventas = QPushButton("🛒 Punto de Venta (Dólar)")
        self.btn_personal = QPushButton("👔 Personal (Admin)")
        self.btn_torniquete = QPushButton("🚪 Torniquete Portería")
        self.btn_logout = QPushButton("🔴 Cerrar Sesión")

        estilo_btn_nav = "background-color: #334155; color: #F8FAFC; padding: 8px 14px; font-weight: bold; border-radius: 6px;"
        self.btn_socios.setStyleSheet(estilo_btn_nav)
        self.btn_clases.setStyleSheet(estilo_btn_nav)
        self.btn_ventas.setStyleSheet(estilo_btn_nav)
        self.btn_personal.setStyleSheet("background-color: #8E44AD; color: #F8FAFC; padding: 8px 14px; font-weight: bold; border-radius: 6px;")
        self.btn_torniquete.setStyleSheet("background-color: #27AE60; color: #F8FAFC; padding: 8px 14px; font-weight: bold; border-radius: 6px;")
        self.btn_logout.setStyleSheet("background-color: #EF4444; color: white; padding: 8px 14px; font-weight: bold; border-radius: 6px;")

        layout_nav.addWidget(self.lbl_usuario_status)
        layout_nav.addStretch()
        layout_nav.addWidget(self.btn_toggle_tema)
        layout_nav.addWidget(self.btn_socios)
        layout_nav.addWidget(self.btn_clases)
        layout_nav.addWidget(self.btn_ventas)
        layout_nav.addWidget(self.btn_personal)
        layout_nav.addWidget(self.btn_torniquete)
        layout_nav.addWidget(self.btn_logout)

        self.layout_principal.addWidget(self.barras_navegacion)
        self.barras_navegacion.setVisible(False)

        # 2. Pila de Pantallas (QStackedWidget)
        self.pantallas = QStackedWidget()

        # Vistas de la aplicación
        self.construir_vista_login()      # Índice 0
        self.construir_vista_socios()     # Índice 1
        self.construir_vista_clases()     # Índice 2
        self.construir_vista_ventas()     # Índice 3
        self.construir_vista_personal()   # Índice 4
        self.construir_vista_torniquete()  # Índice 5

        self.layout_principal.addWidget(self.pantallas)

        # Conectar eventos de botones de navegación
        self.btn_socios.clicked.connect(lambda: self.ir_a_pantalla(1))
        self.btn_clases.clicked.connect(lambda: self.ir_a_pantalla(2))
        self.btn_ventas.clicked.connect(lambda: self.ir_a_pantalla(3))
        self.btn_personal.clicked.connect(lambda: self.ir_a_pantalla(4))
        self.btn_torniquete.clicked.connect(lambda: self.ir_a_pantalla(5))
        self.btn_logout.clicked.connect(self.cerrar_sesion)

        self.statusBar().showMessage("🔒 Por favor inicie sesión para acceder al sistema.")

    def alternar_tema(self):
        self.modo_oscuro_activo = not self.modo_oscuro_activo
        if self.modo_oscuro_activo:
            self.setStyleSheet(self.QSS_MODO_OSCURO)
            self.btn_toggle_tema.setText("☀️ Modo Claro")
            self.btn_toggle_tema.setStyleSheet("background-color: #0284C7; color: white; padding: 6px 12px; font-weight: bold; border-radius: 6px;")
            self.barras_navegacion.setStyleSheet("background-color: #1E293B; border-radius: 8px; padding: 4px;")
            self.lbl_usuario_status.setStyleSheet("font-weight: bold; color: #38BDF8; font-size: 13px;")
            if hasattr(self, "card_login"):
                self.card_login.setStyleSheet("background-color: #1E293B; border-radius: 12px; border: 1px solid #334155;")
            if hasattr(self, "lbl_demo"):
                self.lbl_demo.setStyleSheet("font-size: 11px; color: #CBD5E1; background-color: #0F172A; padding: 8px; border-radius: 6px; border: 1px solid #334155;")
        else:
            self.setStyleSheet(self.QSS_MODO_CLARO)
            self.btn_toggle_tema.setText("🌙 Modo Oscuro")
            self.btn_toggle_tema.setStyleSheet("background-color: #475569; color: white; padding: 6px 12px; font-weight: bold; border-radius: 6px;")
            self.barras_navegacion.setStyleSheet("background-color: #E2E8F0; border-radius: 8px; padding: 4px;")
            self.lbl_usuario_status.setStyleSheet("font-weight: bold; color: #0284C7; font-size: 13px;")
            if hasattr(self, "card_login"):
                self.card_login.setStyleSheet("background-color: #FFFFFF; border-radius: 12px; border: 1px solid #CBD5E1;")
            if hasattr(self, "lbl_demo"):
                self.lbl_demo.setStyleSheet("font-size: 11px; color: #334155; background-color: #F1F5F9; padding: 8px; border-radius: 6px; border: 1px solid #CBD5E1;")

        # Re-aplicar resaltado de pestaña activa
        self.ir_a_pantalla(self.pantallas.currentIndex())

    def ir_a_pantalla(self, idx):
        self.pantallas.setCurrentIndex(idx)
        # Resaltar pestaña activa respetando el tema
        bg_inactive = "#334155" if self.modo_oscuro_activo else "#E2E8F0"
        fg_inactive = "#F8FAFC" if self.modo_oscuro_activo else "#0F172A"
        btn_navs = [(1, self.btn_socios), (2, self.btn_clases), (3, self.btn_ventas)]
        for i, b in btn_navs:
            if i == idx:
                b.setStyleSheet("background-color: #F97316; color: white; padding: 8px 14px; font-weight: bold; border-radius: 6px;")
            else:
                b.setStyleSheet(f"background-color: {bg_inactive}; color: {fg_inactive}; padding: 8px 14px; font-weight: bold; border-radius: 6px;")

    # =========================================================================
    # VISTA 0: LOGIN & AUTENTICACIÓN RBAC
    # =========================================================================
    def construir_vista_login(self):
        self.vista_login = QWidget()
        layout = QVBoxLayout(self.vista_login)
        layout.setAlignment(Qt.AlignCenter)

        # Tarjeta de Login
        self.card_login = QWidget()
        self.card_login.setFixedSize(420, 380)
        self.card_login.setStyleSheet("background-color: #1E293B; border-radius: 12px; border: 1px solid #334155;")
        layout_card = QVBoxLayout(self.card_login)

        lbl_titulo = QLabel("🏋️ PowerFit Gym")
        lbl_subtitulo = QLabel("Autenticación & Control de Acceso (RBAC)")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_subtitulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #F97316;")
        lbl_subtitulo.setStyleSheet("font-size: 12px; color: #94A3B8;")

        form = QFormLayout()
        self.input_login_usuario = QLineEdit()
        self.input_login_password = QLineEdit()
        self.input_login_password.setEchoMode(QLineEdit.Password)

        self.input_login_usuario.setPlaceholderText("Ej: admin, recepcion, instructor")
        self.input_login_password.setPlaceholderText("Contraseña")

        form.addRow("Usuario:", self.input_login_usuario)
        form.addRow("Contraseña:", self.input_login_password)

        btn_ingresar = QPushButton("🔑 Iniciar Sesión")
        btn_ingresar.setStyleSheet("background-color: #F97316; color: white; padding: 12px; font-size: 14px; font-weight: bold; border-radius: 6px;")
        btn_ingresar.clicked.connect(self.iniciar_sesion)

        # Ayuda de credenciales demo
        self.lbl_demo = QLabel(
            "💡 <b>Cuentas de Prueba:</b><br>"
            "• Admin: <code>admin</code> / <code>admin123</code><br>"
            "• Recepción: <code>recepcion</code> / <code>rec123</code><br>"
            "• Instructor: <code>instructor</code> / <code>ins123</code>"
        )
        self.lbl_demo.setStyleSheet("font-size: 11px; padding: 8px; border-radius: 6px; border: 1px solid #334155;")

        layout_card.addWidget(lbl_titulo)
        layout_card.addWidget(lbl_subtitulo)
        layout_card.addSpacing(10)
        layout_card.addLayout(form)
        layout_card.addSpacing(10)
        layout_card.addWidget(btn_ingresar)
        layout_card.addSpacing(10)
        layout_card.addWidget(self.lbl_demo)

        layout.addWidget(self.card_login)
        self.pantallas.addWidget(self.vista_login)

    def iniciar_sesion(self):
        usr = self.input_login_usuario.text().strip()
        pwd = self.input_login_password.text().strip()

        if not usr or not pwd:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor ingresa usuario y contraseña.")
            return

        if usr in self.usuarios_sistema and self.usuarios_sistema[usr].autenticar(pwd):
            self.usuario_actual = self.usuarios_sistema[usr]
            rol = self.usuario_actual.getRol()

            self.lbl_usuario_status.setText(f"👤 {self.usuario_actual.getNombres()} | Rol: {rol}")
            self.barras_navegacion.setVisible(True)

            # Control de Acceso por Roles (RBAC)
            if rol == "Administrador":
                self.btn_socios.setVisible(True)
                self.btn_clases.setVisible(True)
                self.btn_ventas.setVisible(True)
                self.btn_personal.setVisible(True)
                self.ir_a_pantalla(1)  # Ir a Socios
            elif rol == "Recepcionista":
                self.btn_socios.setVisible(True)
                self.btn_clases.setVisible(False)
                self.btn_ventas.setVisible(True)
                self.btn_personal.setVisible(False)
                self.ir_a_pantalla(1)  # Ir a Socios
            elif rol == "Instructor":
                self.btn_socios.setVisible(False)
                self.btn_clases.setVisible(True)
                self.btn_ventas.setVisible(False)
                self.btn_personal.setVisible(False)
                self.ir_a_pantalla(2)  # Ir a Clases

            self.statusBar().showMessage(f"🟢 Sesión iniciada como {self.usuario_actual.getNombres()} ({rol})")
            QMessageBox.information(self, "Acceso Concedido", f"¡Bienvenido/a {self.usuario_actual.getNombres()}!\nRol: {rol}")
        else:
            QMessageBox.critical(self, "Acceso Denegado", "Usuario o contraseña incorrectos.")

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.input_login_usuario.clear()
        self.input_login_password.clear()
        self.barras_navegacion.setVisible(False)
        self.pantallas.setCurrentIndex(0)
        self.statusBar().showMessage("🔒 Sesión cerrada. Por favor inicie sesión.")

    # =========================================================================
    # VISTA 1: GESTIÓN DE SOCIOS
    # =========================================================================
    def construir_vista_socios(self):
        self.vista_socios = QWidget()
        layout_socios = QVBoxLayout(self.vista_socios)

        lbl = QLabel("📋 Registro y Gestión de Socios")
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout_socios.addWidget(lbl)

        form_socios = QFormLayout()
        self.input_rut = QLineEdit()
        self.input_nombres = QLineEdit()
        self.input_apellidos = QLineEdit()
        self.input_telefono = QLineEdit()
        self.input_correo = QLineEdit()

        self.combo_tipo_direccion = QComboBox()
        self.combo_tipo_direccion.addItems(["Casa", "Departamento", "Block", "Otro"])

        self.input_calle = QLineEdit()
        self.input_numero = QLineEdit()
        self.input_referencia = QLineEdit()

        self.combo_comunas = QComboBox()
        comunas_dict = cargar_comunas_ine()
        for id_c, nombre_c in comunas_dict.items():
            self.combo_comunas.addItem(f"{nombre_c} (ID: {id_c})")

        self.combo_estado_inicial = QComboBox()
        self.combo_estado_inicial.addItems(["🟢 Al Día (Vigente 30 días)", "🔴 Vencida / Impago (Requiere Cobro)", "⚪ Plan Cancelado / Inactivo"])

        form_socios.addRow("RUT: ", self.input_rut)
        form_socios.addRow("Nombres: ", self.input_nombres)
        form_socios.addRow("Apellidos: ", self.input_apellidos)
        form_socios.addRow("Teléfono: ", self.input_telefono)
        form_socios.addRow("Correo Electrónico: ", self.input_correo)
        form_socios.addRow("Estado Inicial Membresía: ", self.combo_estado_inicial)
        form_socios.addRow("Tipo Vivienda: ", self.combo_tipo_direccion)
        form_socios.addRow("Calle: ", self.input_calle)
        form_socios.addRow("Número: ", self.input_numero)
        form_socios.addRow("Referencia: ", self.input_referencia)
        form_socios.addRow("Comuna (Chile): ", self.combo_comunas)

        layout_socios.addLayout(form_socios)

        self.btn_guardar_socio = QPushButton("💾 Guardar Socio")
        self.btn_guardar_socio.setStyleSheet("background-color: #27AE60; color: white; padding: 8px; font-weight: bold;")
        self.btn_guardar_socio.clicked.connect(self.guardar_socio)
        layout_socios.addWidget(self.btn_guardar_socio)

        self.tabla_socios = QTableWidget()
        self.tabla_socios.setColumnCount(6)
        self.tabla_socios.setHorizontalHeaderLabels(["RUT", "Nombre Completo", "Teléfono", "Comuna", "Vivienda", "Membresía"])
        layout_socios.addWidget(self.tabla_socios)

        # Botones de Recepción para Cobro y Cancelación
        layout_acciones_socio = QHBoxLayout()
        self.btn_renovar_membresia = QPushButton("💵 Cobrar Mensualidad / Renovar (+30d) - Recepción")
        self.btn_renovar_membresia.setStyleSheet("background-color: #2980B9; color: white; padding: 10px; font-weight: bold;")
        self.btn_renovar_membresia.clicked.connect(self.renovar_membresia_socio)

        self.btn_cancelar_plan = QPushButton("🚫 Cancelar / Desactivar Plan - Recepción")
        self.btn_cancelar_plan.setStyleSheet("background-color: #C0392B; color: white; padding: 10px; font-weight: bold;")
        self.btn_cancelar_plan.clicked.connect(self.cancelar_plan_socio)

        layout_acciones_socio.addWidget(self.btn_renovar_membresia)
        layout_acciones_socio.addWidget(self.btn_cancelar_plan)
        layout_socios.addLayout(layout_acciones_socio)

        self.pantallas.addWidget(self.vista_socios)

    def guardar_socio(self):
        rut = self.input_rut.text().strip()
        nombres = self.input_nombres.text().strip()
        apellidos = self.input_apellidos.text().strip()
        telefono = self.input_telefono.text().strip()
        comuna = self.combo_comunas.currentText()
        tipo_direccion = self.combo_tipo_direccion.currentText()

        if not rut or not nombres or not apellidos:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor completa al menos RUT, Nombres y Apellidos")
            return

        row = self.tabla_socios.rowCount()
        self.tabla_socios.insertRow(row)
        self.tabla_socios.setItem(row, 0, QTableWidgetItem(rut))
        self.tabla_socios.setItem(row, 1, QTableWidgetItem(f"{nombres} {apellidos}"))
        self.tabla_socios.setItem(row, 2, QTableWidgetItem(telefono))
        self.tabla_socios.setItem(row, 3, QTableWidgetItem(comuna))
        self.tabla_socios.setItem(row, 4, QTableWidgetItem(tipo_direccion))

        # Crear objetos Comuna y Direccion integrados
        from src.models import Comuna
        comuna_str = self.combo_comunas.currentText()
        nombre_comuna = comuna_str.split(" (ID:")[0]
        obj_comuna = Comuna(idComuna=13101, nombre=nombre_comuna)

        tipo_dir_mapeo = tipo_direccion.lower()
        if tipo_dir_mapeo not in ["casa", "dpto", "block"]:
            tipo_dir_mapeo = "casa"

        obj_direccion = Direccion(
            idDireccion=len(self.socios_registrados) + 1,
            tipoDireccion=tipo_dir_mapeo,
            calle=self.input_calle.text().strip() or "Sin Calle",
            numero=self.input_numero.text().strip() or "S/N",
            referencia=self.input_referencia.text().strip(),
            comuna=obj_comuna,
        )

        # Evaluar estado inicial seleccionado
        estado_sel = self.combo_estado_inicial.currentText()
        from datetime import date, timedelta
        if "Al Día" in estado_sel:
            fecha_venc = date.today() + timedelta(days=30)
            activo = True
        elif "Vencida" in estado_sel:
            fecha_venc = date.today() - timedelta(days=1)  # Vencida ayer
            activo = True
        else:
            fecha_venc = date.today()
            activo = False

        # Crear y guardar objeto Socio en el dominio POO
        nuevo_socio = Socio(
            idSocio=len(self.socios_registrados) + 1,
            rut=rut,
            nombres=nombres,
            apellidoPaterno=apellidos,
            fechaVencimientoMembresia=fecha_venc,
            estadoActivo=activo,
            apellidoMaterno="",
            telefono=telefono,
            correoElectronico=self.input_correo.text().strip(),
        )
        # Asociar la direccion completa mejorada al socio
        nuevo_socio.direccion = obj_direccion

        # Invocar formalmente registrarSocio() del usuario recepcionista/admin en sesión
        if isinstance(self.usuario_actual, Recepcionista):
            self.usuario_actual.registrarSocio(nuevo_socio)

        self.socios_registrados.append(nuevo_socio)
        
        lbl_estado = "🟢 Al Día" if (nuevo_socio.estadoActivo and nuevo_socio.permitirIngreso()) else ("🔴 Vencida / Impago" if nuevo_socio.estadoActivo else "⚪ Plan Cancelado")
        self.tabla_socios.setItem(row, 5, QTableWidgetItem(lbl_estado))
        self.actualizar_combo_socios_inscripcion()

        QMessageBox.information(
            self,
            "Socio Registrado",
            f"¡Socio {nombres} {apellidos} registrado exitosamente!\n"
            f"📍 Dirección: {obj_direccion.obtenerDireccionCompleta()}\n"
            f"🔑 Estado Membresía: {lbl_estado}"
        )

    def renovar_membresia_socio(self):
        items = self.tabla_socios.selectedItems()
        if not items:
            QMessageBox.warning(self, "Selección Requerida", "Por favor selecciona un socio en la tabla para renovar su membresía.")
            return

        row = items[0].row()
        rut_socio = self.tabla_socios.item(row, 0).text()
        socio = next((s for s in self.socios_registrados if s.getRut() == rut_socio), None)

        if socio:
            from datetime import date, timedelta
            # Invocar Recepcionista.cobrarMensualidad
            if isinstance(self.usuario_actual, Recepcionista):
                self.usuario_actual.cobrarMensualidad(socio, 35000)
            
            socio.renovarMembresia(dias=30)
            self.tabla_socios.setItem(row, 5, QTableWidgetItem("🟢 Al Día (+30d)"))
            QMessageBox.information(
                self,
                "Membresía Renovada",
                f"¡Cobro realizado por la Recepcion! La membresía del socio {socio.getNombres()} ha sido renovada hasta {socio.fechaVencimientoMembresia}."
            )

    def cancelar_plan_socio(self):
        items = self.tabla_socios.selectedItems()
        if not items:
            QMessageBox.warning(self, "Selección Requerida", "Por favor selecciona un socio en la tabla para cancelar su plan.")
            return

        row = items[0].row()
        rut_socio = self.tabla_socios.item(row, 0).text()
        socio = next((s for s in self.socios_registrados if s.getRut() == rut_socio), None)

        if socio:
            socio.cancelarPlan()
            self.tabla_socios.setItem(row, 5, QTableWidgetItem("⚪ Plan Cancelado"))
            QMessageBox.warning(
                self,
                "Plan Cancelado",
                f"El plan del socio {socio.getNombres()} ({socio.getRut()}) ha sido CANCELADO/DESACTIVADO.\n"
                f"El molinete de portería bloqueará su ingreso hasta un nuevo alta/renovación."
            )

    # =========================================================================
    # VISTA 2: CLASES DIRIGIDAS & MAPA VISUAL DE SALA
    # =========================================================================
    def construir_vista_clases(self):
        self.vista_clases = QWidget()
        layout_principal_clases = QHBoxLayout(self.vista_clases)

        # Panel Izquierdo: Formulario de Creación y Selección de Socios
        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout(panel_izquierdo)

        lbl = QLabel("🏋️ Clases Dirigidas (Spinning, Yoga, Crossfit)")
        lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #2C3E50;")
        layout_izquierdo.addWidget(lbl)

        form_clases = QFormLayout()
        self.combo_disciplina = QComboBox()
        self.combo_disciplina.addItems(["Spinning", "Yoga", "Crossfit"])

        self.input_nombre_clase = QLineEdit()
        self.input_cupo_maximo = QLineEdit("12")
        self.input_duracion = QLineEdit("60")
        self.input_sala = QLineEdit("Sala 1")

        form_clases.addRow("Disciplina: ", self.combo_disciplina)
        form_clases.addRow("Nombre Clase: ", self.input_nombre_clase)
        form_clases.addRow("Cupo Máximo (Puestos): ", self.input_cupo_maximo)
        form_clases.addRow("Duración (minutos): ", self.input_duracion)
        form_clases.addRow("Sala: ", self.input_sala)

        layout_izquierdo.addLayout(form_clases)

        self.btn_guardar_clase = QPushButton("📌 Crear Clase y Generar Sala")
        self.btn_guardar_clase.setStyleSheet("background-color: #D35400; color: white; padding: 8px; font-weight: bold;")
        self.btn_guardar_clase.clicked.connect(self.guardar_clase)
        layout_izquierdo.addWidget(self.btn_guardar_clase)

        # Sección para Inscribir Socio
        box_inscripcion = QGroupBox("✍️ Inscripción de Socio a Puesto")
        layout_inscripcion = QVBoxLayout(box_inscripcion)

        form_ins = QFormLayout()
        self.combo_socio_inscripcion = QComboBox()
        self.actualizar_combo_socios_inscripcion()

        form_ins.addRow("Socio Seleccionado: ", self.combo_socio_inscripcion)
        layout_inscripcion.addLayout(form_ins)

        lbl_instruccion = QLabel("💡 Selecciona un socio arriba y haz clic en un puesto VERDE (disponible) en el mapa de la derecha para reservarlo.")
        lbl_instruccion.setWordWrap(True)
        lbl_instruccion.setStyleSheet("font-size: 11px; color: #555; background-color: #EAECEE; padding: 6px; border-radius: 4px;")
        layout_inscripcion.addWidget(lbl_instruccion)

        layout_izquierdo.addWidget(box_inscripcion)

        self.tabla_clases = QTableWidget()
        self.tabla_clases.setColumnCount(5)
        self.tabla_clases.setHorizontalHeaderLabels(["Disciplina", "Nombre", "Ocupación", "Sala", "Estado"])
        self.tabla_clases.itemSelectionChanged.connect(self.al_seleccionar_clase_tabla)
        layout_izquierdo.addWidget(self.tabla_clases)

        layout_principal_clases.addWidget(panel_izquierdo, stretch=1)

        # Panel Derecho: Distribución Visual de la Sala (Grid de Puestos)
        self.group_mapa_sala = QGroupBox("🗺️ Mapa y Distribución Visual de Sala en Tiempo Real")
        self.layout_derecho_mapa = QVBoxLayout(self.group_mapa_sala)

        self.lbl_info_sala = QLabel("👈 Crea o selecciona una clase para ver el plano de la sala.")
        self.lbl_info_sala.setStyleSheet("font-weight: bold; color: #7F8C8D;")
        self.layout_derecho_mapa.addWidget(self.lbl_info_sala)

        self.grid_puestos_container = QWidget()
        self.layout_grid_puestos = QGridLayout(self.grid_puestos_container)
        self.layout_derecho_mapa.addWidget(self.grid_puestos_container)

        self.layout_derecho_mapa.addStretch()
        layout_principal_clases.addWidget(self.group_mapa_sala, stretch=1)

        self.pantallas.addWidget(self.vista_clases)

    def actualizar_combo_socios_inscripcion(self):
        self.combo_socio_inscripcion.clear()
        if not self.socios_registrados:
            self.combo_socio_inscripcion.addItem("No hay socios registrados")
        else:
            for s in self.socios_registrados:
                self.combo_socio_inscripcion.addItem(f"{s.getNombres()} {s.getApellidoPaterno()} ({s.getRut()})")

    def guardar_clase(self):
        disc = self.combo_disciplina.currentText()
        nombre = self.input_nombre_clase.text().strip()
        cupos_str = self.input_cupo_maximo.text().strip()
        duracion_str = self.input_duracion.text().strip()
        sala = self.input_sala.text().strip()

        if not nombre or not cupos_str:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor ingresa Nombre y Cupos de la clase.")
            return

        try:
            cupos_max = int(cupos_str)
            duracion = int(duracion_str)
        except ValueError:
            QMessageBox.warning(self, "Valor Inválido", "Cupos y Duración deben ser números enteros.")
            return

        # Instanciar según la disciplina (Patrón Polimórfico POO)
        codigo = f"CLS-{len(self.clases_registradas)+1:03d}"
        if disc == "Spinning":
            obj_clase = ClaseSpinning(codigo=codigo, nombre=nombre, cupoMaximo=cupos_max, duracionMin=duracion, sala=sala)
        elif disc == "Yoga":
            obj_clase = ClaseYoga(codigo=codigo, nombre=nombre, cupoMaximo=cupos_max, duracionMin=duracion, sala=sala)
        else:
            obj_clase = ClaseCrossfit(codigo=codigo, nombre=nombre, cupoMaximo=cupos_max, duracionMin=duracion, sala=sala)

        self.clases_registradas[nombre] = obj_clase
        self.clase_seleccionada_actual = obj_clase

        # Insertar en Tabla Visual
        row = self.tabla_clases.rowCount()
        self.tabla_clases.insertRow(row)
        self.tabla_clases.setItem(row, 0, QTableWidgetItem(f"{obj_clase.obtener_icono_disciplina()} {disc}"))
        self.tabla_clases.setItem(row, 1, QTableWidgetItem(nombre))
        self.tabla_clases.setItem(row, 2, QTableWidgetItem(f"0 / {cupos_max} (0%)"))
        self.tabla_clases.setItem(row, 3, QTableWidgetItem(sala))
        self.tabla_clases.setItem(row, 4, QTableWidgetItem("🟢 Disponible"))

        # Renderizar mapa de sala
        self.renderizar_mapa_sala(obj_clase)
        QMessageBox.information(self, "Clase Creada", f"¡Clase '{nombre}' ({disc}) creada en {sala} con {cupos_max} puestos!")

    def al_seleccionar_clase_tabla(self):
        items = self.tabla_clases.selectedItems()
        if items:
            row = items[0].row()
            nombre_clase = self.tabla_clases.item(row, 1).text()
            if nombre_clase in self.clases_registradas:
                self.clase_seleccionada_actual = self.clases_registradas[nombre_clase]
                self.renderizar_mapa_sala(self.clase_seleccionada_actual)

    def renderizar_mapa_sala(self, obj_clase):
        # Limpiar el grid anterior
        for i in reversed(range(self.layout_grid_puestos.count())):
            w = self.layout_grid_puestos.itemAt(i).widget()
            if w is not None:
                w.setParent(None)

        icono = obj_clase.obtener_icono_disciplina()
        self.group_mapa_sala.setTitle(f"🗺️ Mapa Visual de {obj_clase.sala} - {obj_clase.nombre} ({icono})")
        self.lbl_info_sala.setText(
            f"<b>Ocupación:</b> {obj_clase.cupos_ocupados}/{obj_clase.cupo_maximo} Puestos "
            f"({obj_clase.porcentaje_ocupacion:.1f}%) | <b>Disponibles:</b> {obj_clase.cupos_disponibles}"
        )

        # Dibujar matriz de puestos (4 columnas por fila)
        columnas = 4
        for pos in range(obj_clase.cupo_maximo):
            row = pos // columnas
            col = pos % columnas

            socio = obj_clase.cupos[pos]
            btn_puesto = QPushButton()

            if socio is None:
                # Puesto Libre
                btn_puesto.setText(f"{icono}\nPuesto {pos+1}\n[Libre]")
                btn_puesto.setStyleSheet(
                    "background-color: #2ECC71; color: white; font-weight: bold; border-radius: 6px; padding: 10px;"
                )
                btn_puesto.setToolTip(f"Haga clic para inscribir al socio seleccionado en el Puesto {pos+1}")
                btn_puesto.clicked.connect(lambda checked=False, p=pos: self.hacer_clic_puesto(p, inscribir=True))
            else:
                # Puesto Ocupado
                btn_puesto.setText(f"🔴\nPuesto {pos+1}\n{socio.getNombres()}")
                btn_puesto.setStyleSheet(
                    "background-color: #E74C3C; color: white; font-weight: bold; border-radius: 6px; padding: 10px;"
                )
                btn_puesto.setToolTip(f"Ocupado por: {socio.getNombres()} ({socio.getRut()})\nHaga clic para liberar puesto.")
                btn_puesto.clicked.connect(lambda checked=False, p=pos: self.hacer_clic_puesto(p, inscribir=False))

            self.layout_grid_puestos.addWidget(btn_puesto, row, col)

    def hacer_clic_puesto(self, posicion, inscribir=True):
        if not self.clase_seleccionada_actual:
            return

        if inscribir:
            idx_socio = self.combo_socio_inscripcion.currentIndex()
            if idx_socio < 0 or not self.socios_registrados:
                QMessageBox.warning(self, "Sin Socios", "Debes registrar al menos un socio en la pestaña de Socios antes de inscribir.")
                return

            socio = self.socios_registrados[idx_socio]

            # Regla de Bloqueo #2 (UML): socio.permitirIngreso()
            if not socio.permitirIngreso():
                QMessageBox.critical(
                    self,
                    "Acceso Denegado (Membresía Vencida)",
                    f"⛔ El socio {socio.getNombres()} ({socio.getRut()}) tiene la membresía VENCIDA.\n"
                    f"La Recepcionista debe realizar el pago/cobro de mensualidad antes de otorgar un cupo."
                )
                return

            exito = self.clase_seleccionada_actual.inscribir_socio(socio, posicion)
            if exito:
                QMessageBox.information(
                    self,
                    "Reserva Exitosa",
                    f"¡{socio.getNombres()} inscrito en el Puesto {posicion+1} para {self.clase_seleccionada_actual.nombre}!"
                )
        else:
            # Liberar puesto
            respuesta = QMessageBox.question(
                self,
                "Liberar Puesto",
                f"¿Deseas cancelar la reserva del Puesto {posicion+1}?",
                QMessageBox.Yes | QMessageBox.No
            )
            if respuesta == QMessageBox.Yes:
                self.clase_seleccionada_actual.liberar_posicion(posicion)

        # Actualizar vista y tabla
        self.actualizar_fila_tabla_clase(self.clase_seleccionada_actual)
        self.renderizar_mapa_sala(self.clase_seleccionada_actual)

    def actualizar_fila_tabla_clase(self, obj_clase):
        for row in range(self.tabla_clases.rowCount()):
            if self.tabla_clases.item(row, 1).text() == obj_clase.nombre:
                self.tabla_clases.setItem(
                    row, 2, QTableWidgetItem(f"{obj_clase.cupos_ocupados} / {obj_clase.cupo_maximo} ({obj_clase.porcentaje_ocupacion:.0f}%)")
                )
                estado = "🔴 Llena" if obj_clase.cupos_disponibles == 0 else "🟢 Disponible"
                self.tabla_clases.setItem(row, 4, QTableWidgetItem(estado))
                break

    # =========================================================================
    # VISTA 3: PUNTO DE VENTA & API DÓLAR
    # =========================================================================
    def construir_vista_ventas(self):
        self.vista_ventas = QWidget()
        layout_ventas = QVBoxLayout(self.vista_ventas)

        lbl = QLabel("🛒 Punto de Venta de Suplementos & API Dólar")
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout_ventas.addWidget(lbl)

        form_ventas = QFormLayout()
        self.combo_producto = QComboBox()
        self.combo_producto.addItems([
            "Proteína Whey Gold 1kg ($45 USD)",
            "Creatina Monohidratada 500g ($25 USD)",
            "Pre-Entreno C4 300g ($30 USD)",
            "BCAA Aminoácidos 400g ($20 USD)",
        ])

        self.input_cantidad = QLineEdit("1")
        self.input_valor_dolar = QLineEdit()
        self.input_valor_dolar.setPlaceholderText("Ej: 950 (Valor CLP del dólar)")

        self.btn_obtener_dolar = QPushButton("🌐 Cargar Dólar Oficial en Vivo")
        self.btn_obtener_dolar.setStyleSheet("background-color: #16A095; color: white; padding: 5px")
        self.btn_obtener_dolar.clicked.connect(self.cargar_dolar_api)

        form_ventas.addRow("Producto Suplemento: ", self.combo_producto)
        form_ventas.addRow("Cantidad a vender: ", self.input_cantidad)
        form_ventas.addRow("Valor dólar (CLP): ", self.input_valor_dolar)
        form_ventas.addRow("Consultar API: ", self.btn_obtener_dolar)

        layout_ventas.addLayout(form_ventas)

        self.btn_guardar_venta = QPushButton("💳 Procesar Venta")
        self.btn_guardar_venta.setStyleSheet("background-color: #2980B9; color: white; padding: 8px; font-weight: bold;")
        self.btn_guardar_venta.clicked.connect(self.guardar_venta)
        layout_ventas.addWidget(self.btn_guardar_venta)

        # Sección Administrador: Reponer Stock (UML Administrador.reponerStock)
        box_admin_stock = QGroupBox("📦 Gestión de Inventario & Reposición (Administrador)")
        layout_stock = QHBoxLayout(box_admin_stock)
        self.input_reponer_cant = QLineEdit("50")
        self.input_reponer_cant.setPlaceholderText("Cantidad a reponer")
        self.btn_reponer_stock = QPushButton("➕ Reponer Stock (Admin)")
        self.btn_reponer_stock.setStyleSheet("background-color: #8E44AD; color: white; font-weight: bold; padding: 6px;")
        self.btn_reponer_stock.clicked.connect(self.reponer_stock_admin)
        layout_stock.addWidget(QLabel("Cantidad:"))
        layout_stock.addWidget(self.input_reponer_cant)
        layout_stock.addWidget(self.btn_reponer_stock)
        layout_ventas.addWidget(box_admin_stock)

        self.tabla_ventas = QTableWidget()
        self.tabla_ventas.setColumnCount(4)
        self.tabla_ventas.setHorizontalHeaderLabels(["Producto", "Cantidad", "Valor Dólar", "Total Estimado (CLP)"])
        layout_ventas.addWidget(self.tabla_ventas)

        self.pantallas.addWidget(self.vista_ventas)

    def reponer_stock_admin(self):
        if not isinstance(self.usuario_actual, Administrador):
            QMessageBox.warning(self, "Acceso Denegado", "Solo el Administrador posee permisos para reponer stock físico.")
            return

        cant_str = self.input_reponer_cant.text().strip()
        try:
            cant = int(cant_str)
        except ValueError:
            QMessageBox.warning(self, "Valor Inválido", "La cantidad a reponer debe ser un número entero.")
            return

        prod_nombre = self.combo_producto.currentText()
        precio_usd = 45.0 if "Whey" in prod_nombre else (25.0 if "Creatina" in prod_nombre else (30.0 if "Pre-Entreno" in prod_nombre else 20.0))
        sup = Suplemento("SUP-001", prod_nombre, precio_usd, stock=20)

        # Invocar Administrador.reponerStock(sup, cant)
        self.usuario_actual.reponerStock(sup, cant)
        QMessageBox.information(
            self,
            "Stock Repuesto",
            f"¡El Administrador {self.usuario_actual.getNombres()} ha repuesto +{cant} unidades de '{prod_nombre}'!\n"
            f"Nuevo Stock Total: {sup.stock} unidades."
        )

    def cargar_dolar_api(self):
        try:
            url = "https://mindicador.cl/api/dolar"
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode())
                valor_dolar = data["serie"][0]["valor"]
                self.input_valor_dolar.setText(str(valor_dolar))
                QMessageBox.information(self, "API Dólar Cargar", f"Tasa Oficial del Dólar: ${valor_dolar} CLP")
        except Exception as e:
            QMessageBox.warning(self, "Error API Dólar", f"No se pudo consultar el valor del dólar: {e}")

    def guardar_venta(self):
        prod = self.combo_producto.currentText()
        cant_str = self.input_cantidad.text().strip()
        dolar_clp_str = self.input_valor_dolar.text().strip()

        if not cant_str or not dolar_clp_str:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor ingresa cantidad y valor del dólar en CLP.")
            return

        try:
            cant = int(cant_str)
            valor_dolar = float(dolar_clp_str)
        except ValueError:
            QMessageBox.warning(self, "Valor Inválido", "Cantidad debe ser entero y valor dólar numérico.")
            return

        # 1. Crear Suplemento (UML)
        precio_usd = 45.0 if "Whey" in prod else (25.0 if "Creatina" in prod else (30.0 if "Pre-Entreno" in prod else 20.0))
        cod_prod = "SUP-001" if "Whey" in prod else ("SUP-002" if "Creatina" in prod else "SUP-003")
        obj_suplemento = Suplemento(codigo=cod_prod, nombre=prod, precioUSD=precio_usd, stock=100)

        # 2. Verificar Stock (Regla #6 UML)
        if not obj_suplemento.hayStock(cant):
            QMessageBox.warning(self, "Stock Insuficiente", f"No hay stock suficiente para {prod}.")
            return

        precio_clp = obj_suplemento.calcularPrecioCLP(valor_dolar)

        # 3. Crear DetalleVenta y Venta compuesta (UML)
        obj_detalle = DetalleVenta(cantidad=cant, precioUnitarioCLP=precio_clp, suplemento=obj_suplemento)
        obj_venta = Venta(numero=self.tabla_ventas.rowCount() + 1)
        exito = obj_venta.agregarDetalle(obj_detalle)

        # 4. Invocar Recepcionista.registrarVenta(venta) si corresponde (UML)
        if isinstance(self.usuario_actual, Recepcionista):
            self.usuario_actual.registrarVenta(obj_venta)

        row = self.tabla_ventas.rowCount()
        self.tabla_ventas.insertRow(row)
        self.tabla_ventas.setItem(row, 0, QTableWidgetItem(prod))
        self.tabla_ventas.setItem(row, 1, QTableWidgetItem(str(cant)))
        self.tabla_ventas.setItem(row, 2, QTableWidgetItem(f"${valor_dolar:,.2f} CLP"))
        self.tabla_ventas.setItem(row, 3, QTableWidgetItem(f"${obj_venta.totalCLP:,.0f} CLP"))

        QMessageBox.information(
            self,
            "Venta Transaccional Procesada",
            f"¡Venta N° {obj_venta.numero} de '{prod}' procesada con éxito!\n"
            f"💰 Total CLP: ${obj_venta.totalCLP:,.0f}\n"
            f"📦 Stock Restante: {obj_suplemento.stock} unidades"
        )

    # =========================================================================
    # VISTA 4: GESTIÓN DE PERSONAL / TRABAJADORES (ADMINISTRADOR)
    # =========================================================================
    def construir_vista_personal(self):
        self.vista_personal = QWidget()
        layout_personal = QVBoxLayout(self.vista_personal)

        lbl = QLabel("👔 Alta y Registro de Personal (Administrador)")
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #8E44AD;")
        layout_personal.addWidget(lbl)

        form_personal = QFormLayout()
        self.input_trab_rut = QLineEdit()
        self.input_trab_nombres = QLineEdit()
        self.input_trab_apellidos = QLineEdit()
        self.input_trab_usuario = QLineEdit()
        self.input_trab_pass = QLineEdit()
        self.input_trab_pass.setEchoMode(QLineEdit.Password)

        self.combo_trab_rol = QComboBox()
        self.combo_trab_rol.addItems(["Recepcionista", "Instructor", "Administrador"])

        form_personal.addRow("Rol a Asignar: ", self.combo_trab_rol)
        form_personal.addRow("RUT: ", self.input_trab_rut)
        form_personal.addRow("Nombres: ", self.input_trab_nombres)
        form_personal.addRow("Apellidos: ", self.input_trab_apellidos)
        form_personal.addRow("Nombre Usuario: ", self.input_trab_usuario)
        form_personal.addRow("Contraseña: ", self.input_trab_pass)

        layout_personal.addLayout(form_personal)

        self.btn_guardar_trabajador = QPushButton("➕ Crear Trabajador (Invoca Admin.crearTrabajador)")
        self.btn_guardar_trabajador.setStyleSheet("background-color: #8E44AD; color: white; padding: 10px; font-weight: bold;")
        self.btn_guardar_trabajador.clicked.connect(self.guardar_trabajador_admin)
        layout_personal.addWidget(self.btn_guardar_trabajador)

        self.tabla_personal = QTableWidget()
        self.tabla_personal.setColumnCount(4)
        self.tabla_personal.setHorizontalHeaderLabels(["ID", "Usuario", "Nombre Completo", "Rol"])
        layout_personal.addWidget(self.tabla_personal)

        # Cargar trabajadores por defecto
        for u in self.usuarios_sistema.values():
            r = self.tabla_personal.rowCount()
            self.tabla_personal.insertRow(r)
            self.tabla_personal.setItem(r, 0, QTableWidgetItem(str(u.idTrabajador)))
            self.tabla_personal.setItem(r, 1, QTableWidgetItem(u.usuario))
            self.tabla_personal.setItem(r, 2, QTableWidgetItem(f"{u.nombres} {u.apellidoPaterno}"))
            self.tabla_personal.setItem(r, 3, QTableWidgetItem(u.getRol()))

        self.pantallas.addWidget(self.vista_personal)

    def guardar_trabajador_admin(self):
        if not isinstance(self.usuario_actual, Administrador):
            QMessageBox.warning(self, "Acceso Denegado", "Solo un Administrador posee permisos para crear personal.")
            return

        rol = self.combo_trab_rol.currentText()
        rut = self.input_trab_rut.text().strip()
        nombres = self.input_trab_nombres.text().strip()
        apellidos = self.input_trab_apellidos.text().strip()
        usr = self.input_trab_usuario.text().strip()
        pwd = self.input_trab_pass.text().strip()

        if not rut or not nombres or not usr or not pwd:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor completa RUT, Nombres, Usuario y Contraseña.")
            return

        nuevo_id = str(len(self.usuarios_sistema) + 1)
        if rol == "Recepcionista":
            nuevo_t = Recepcionista(
                idTrabajador=nuevo_id, rut=rut, nombres=nombres, apellidoPaterno=apellidos, usuario=usr, passHash=pwd
            )
        elif rol == "Instructor":
            nuevo_t = Instructor(
                especialidad="Fitness", idTrabajador=nuevo_id, rut=rut, nombres=nombres, apellidoPaterno=apellidos, usuario=usr, passHash=pwd
            )
        else:
            nuevo_t = Administrador(
                nivelAcceso="General", idTrabajador=nuevo_id, rut=rut, nombres=nombres, apellidoPaterno=apellidos, usuario=usr, passHash=pwd
            )

        # Invocar formalmente Administrador.crearTrabajador(t)
        exito = self.usuario_actual.crearTrabajador(nuevo_t)
        if exito:
            self.usuarios_sistema[usr] = nuevo_t
            r = self.tabla_personal.rowCount()
            self.tabla_personal.insertRow(r)
            self.tabla_personal.setItem(r, 0, QTableWidgetItem(str(nuevo_t.idTrabajador)))
            self.tabla_personal.setItem(r, 1, QTableWidgetItem(nuevo_t.usuario))
            self.tabla_personal.setItem(r, 2, QTableWidgetItem(f"{nuevo_t.nombres} {nuevo_t.apellidoPaterno}"))
            self.tabla_personal.setItem(r, 3, QTableWidgetItem(nuevo_t.getRol()))

            QMessageBox.information(
                self,
                "Trabajador Creado",
                f"¡El Administrador {self.usuario_actual.getNombres()} ha creado al trabajador {nombres} con rol {rol}!"
            )

    # =========================================================================
    # VISTA 5: SIMULADOR DE TORNIQUETE / CONTROL DE PORTERÍA
    # =========================================================================
    def construir_vista_torniquete(self):
        self.vista_torniquete = QWidget()
        layout_torniquete = QVBoxLayout(self.vista_torniquete)

        lbl = QLabel("🚪 Simulador de Torniquete & Control de Acceso (Portería)")
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #27AE60;")
        layout_torniquete.addWidget(lbl)

        # Panel de Lectura de RUT
        group_lector = QGroupBox("📱 Lector de RUT / Escáner de Credencial")
        layout_lector = QVBoxLayout(group_lector)

        form_lector = QFormLayout()
        self.input_rut_torniquete = QLineEdit()
        self.input_rut_torniquete.setPlaceholderText("Ej: 12.345.678-5")
        form_lector.addRow("RUT Socio: ", self.input_rut_torniquete)

        btn_simular_paso = QPushButton("🔔 Simular Lectura de Torniquete (Invoca Socio.permitirIngreso)")
        btn_simular_paso.setStyleSheet("background-color: #27AE60; color: white; padding: 12px; font-weight: bold; font-size: 14px;")
        btn_simular_paso.clicked.connect(self.simular_torniquete)

        layout_lector.addLayout(form_lector)
        layout_lector.addWidget(btn_simular_paso)
        layout_torniquete.addWidget(group_lector)

        # Pantalla Visual del Estado del Molinete
        self.card_estado_molinete = QWidget()
        self.card_estado_molinete.setStyleSheet("background-color: #1E293B; border-radius: 10px; border: 2px solid #334155;")
        layout_molinete = QVBoxLayout(self.card_estado_molinete)

        self.lbl_icono_torniquete = QLabel("🔒")
        self.lbl_icono_torniquete.setAlignment(Qt.AlignCenter)
        self.lbl_icono_torniquete.setStyleSheet("font-size: 64px;")

        self.lbl_estado_molinete = QLabel("ESPERANDO LECTURA EN PORTERÍA")
        self.lbl_estado_molinete.setAlignment(Qt.AlignCenter)
        self.lbl_estado_molinete.setStyleSheet("font-size: 18px; font-weight: bold; color: #94A3B8;")

        self.lbl_detalle_socio_torniquete = QLabel("Ingrese RUT arriba para verificar estado de membresía en tiempo real.")
        self.lbl_detalle_socio_torniquete.setAlignment(Qt.AlignCenter)
        self.lbl_detalle_socio_torniquete.setStyleSheet("font-size: 13px; color: #CBD5E1;")

        layout_molinete.addWidget(self.lbl_icono_torniquete)
        layout_molinete.addWidget(self.lbl_estado_molinete)
        layout_molinete.addWidget(self.lbl_detalle_socio_torniquete)

        layout_torniquete.addWidget(self.card_estado_molinete)
        self.pantallas.addWidget(self.vista_torniquete)

    def simular_torniquete(self):
        rut = self.input_rut_torniquete.text().strip()
        if not rut:
            QMessageBox.warning(self, "RUT Vacío", "Por favor ingresa un RUT para validar el molinete.")
            return

        socio = next((s for s in self.socios_registrados if s.getRut().replace(".", "").replace("-", "").upper() == rut.replace(".", "").replace("-", "").upper()), None)

        if not socio:
            self.lbl_icono_torniquete.setText("⚠️")
            self.lbl_estado_molinete.setText("SOCIO NO ENCONTRADO EN SISTEMA")
            self.lbl_estado_molinete.setStyleSheet("font-size: 18px; font-weight: bold; color: #F1C40F;")
            self.lbl_detalle_socio_torniquete.setText(f"El RUT {rut} no registra inscripción en PowerFit.")
            self.card_estado_molinete.setStyleSheet("background-color: #7D6608; border-radius: 10px; border: 2px solid #F1C40F;")
            return

        # Invocar formalmente la regla de negocio UML: Socio.permitirIngreso()
        permitido = socio.permitirIngreso()

        if permitido:
            self.lbl_icono_torniquete.setText("🟢 PASE CONCEDIDO")
            self.lbl_estado_molinete.setText("TORNIQUETE DESBLOQUEADO - ¡BIENVENIDO/A!")
            self.lbl_estado_molinete.setStyleSheet("font-size: 18px; font-weight: bold; color: #2ECC71;")
            self.lbl_detalle_socio_torniquete.setText(
                f"Socio: {socio.getNombres()} {socio.getApellidoPaterno()} | RUT: {socio.getRut()}\n"
                f"Membresía Al Día hasta: {socio.fechaVencimientoMembresia}"
            )
            self.card_estado_molinete.setStyleSheet("background-color: #145A32; border-radius: 10px; border: 2px solid #2ECC71;")
            
            QMessageBox.information(
                self,
                "🟢 Torniquete Desbloqueado",
                f"¡Pase Concedido!\nSocio: {socio.getNombres()} {socio.getApellidoPaterno()}\n"
                f"Vigencia: Hasta {socio.fechaVencimientoMembresia}"
            )
        else:
            self.lbl_icono_torniquete.setText("🔴 ACCESO DENEGADO")
            self.lbl_estado_molinete.setText("TORNIQUETE BLOQUEADO - MEMBRESÍA VENCIDA / PLAN CANCELADO")
            self.lbl_estado_molinete.setStyleSheet("font-size: 18px; font-weight: bold; color: #E74C3C;")
            
            motivo = "Membresía VENCIDA / IMPAGO" if socio.estadoActivo else "Plan CANCELADO / INACTIVO"
            self.lbl_detalle_socio_torniquete.setText(
                f"Socio: {socio.getNombres()} {socio.getApellidoPaterno()} | RUT: {socio.getRut()}\n"
                f"⛔ Estado: {motivo} ({socio.fechaVencimientoMembresia}). Pasar a Recepción a regularizar pago."
            )
            self.card_estado_molinete.setStyleSheet("background-color: #641E16; border-radius: 10px; border: 2px solid #E74C3C;")

            # 🚨 Popup Alerta Flotante en Pantalla
            QMessageBox.critical(
                self,
                "🚨 ALERTA PORTERÍA: TORNIQUETE BLOQUEADO",
                f"⛔ ACCESO RECHAZADO EN PORTERÍA\n\n"
                f"👤 Socio: {socio.getNombres()} {socio.getApellidoPaterno()}\n"
                f"📄 RUT: {socio.getRut()}\n"
                f"⚠️ Motivo Bloqueo: {motivo}\n"
                f"📅 Fecha Vencimiento: {socio.fechaVencimientoMembresia}\n\n"
                f"📢 El molinete ha sido bloqueado automáticamente.\nPor favor indique al socio dirijirse al módulo de Recepción para realizar el cobro/renovación."
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipalPowerFit()
    ventana.show()
    sys.exit(app.exec())