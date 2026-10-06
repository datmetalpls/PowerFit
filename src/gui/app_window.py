"""PowerFit - Punto de entrada principal con Autenticación y Control de Acceso por Roles (RBAC - Hito 6)."""
import os
import sys
import json
import urllib.request

from src.dao.conexion import ConexionDB
from src.dao.socio_dao import SocioDAO
from src.dao.trabajador_dao import TrabajadorDAO
from src.dao.clase_dao import ClaseDAO
from src.dao.suplemento_dao import SuplementoDAO
from src.dao.inscripcion_dao import InscripcionDAO
from src.dao.venta_dao import VentaDAO


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
    Administrador,
    Instructor,
    Recepcionista,
    Socio,
)


class VentanaPrincipalPowerFit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.intentos_login = 0
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


        #Inicializar base de datos SQLite y DAOss
        ConexionDB.crear_tablas()
        self.socio_dao = SocioDAO()
        self.trabajador_dao = TrabajadorDAO()
        self.clase_dao = ClaseDAO()
        self.suplemento_dao = SuplementoDAO()
        self.inscripcion_dao = InscripcionDAO()
        self.venta_dao = VentaDAO()

        

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

        # Cargar datos de la base de datos SQLite y poblar la GUI
        self.cargar_datos_desde_bd()

        self.layout_principal.addWidget(self.pantallas)

        # Conectar eventos de botones de navegación
        self.btn_socios.clicked.connect(lambda: self.ir_a_pantalla(1))
        self.btn_clases.clicked.connect(lambda: self.ir_a_pantalla(2))
        self.btn_ventas.clicked.connect(lambda: self.ir_a_pantalla(3))
        self.btn_personal.clicked.connect(lambda: self.ir_a_pantalla(4))
        self.btn_torniquete.clicked.connect(lambda: self.ir_a_pantalla(5))
        self.btn_logout.clicked.connect(self.cerrar_sesion)

        self.statusBar().showMessage("🔒 Por favor inicie sesión para acceder al sistema.")

    def cargar_datos_desde_bd(self):
        """Carga y sincroniza la memoria local y las tablas de la GUI con la base de datos SQLite."""
        # 1. Cargar socios desde SQLite y refrescar tabla visual
        self.socios_registrados = self.socio_dao.obtener_todos()
        if hasattr(self, 'actualizar_tabla_socios'):
            self.actualizar_tabla_socios()

        # 2. Cargar clases dirigidas desde SQLite y refrescar tabla visual
        clases_list = self.clase_dao.obtener_todos()
        self.clases_registradas = {clase.nombre: clase for clase in clases_list}
        if hasattr(self, 'actualizar_tabla_clases_bd'):
            self.actualizar_tabla_clases_bd()

        # 3. Cargar usuarios del sistema y refrescar tabla visual de personal
        trabajadores_bd = self.trabajador_dao.obtener_todos()
        if not trabajadores_bd:
            for user_obj in self.usuarios_sistema.values():
                self.trabajador_dao.guardar(user_obj)
            trabajadores_bd = self.trabajador_dao.obtener_todos()

        pass_map = {"admin": "admin123", "recepcion": "rec123", "instructor": "ins123"}
        for t in trabajadores_bd:
            key_user = getattr(t, 'usuario', None) or t.nombres.lower().replace(" ", "")
            if key_user in pass_map:
                t._passHash = pass_map[key_user]
            self.usuarios_sistema[key_user] = t
        if hasattr(self, 'actualizar_tabla_personal'):
            self.actualizar_tabla_personal()

        # 4. Cargar inventario y ventas persistidos en la BD
        if hasattr(self, 'actualizar_inventario_y_combo'):
            self.actualizar_inventario_y_combo()
        self.cargar_historial_ventas_bd()


    def desbloquear_trabajador_admin(self):
        filas = self.tabla_personal.selectionModel().selectedRows()
        if not filas:
            QMessageBox.warning(self, "Selección Vacía", "Debes seleccionar un trabajador de la tabla para desbloquear.")
            return
        
        usuario_sel = self.tabla_personal.item(filas[0].row(), 1).text()
        if usuario_sel in self.usuarios_sistema:
            t = self.usuarios_sistema[usuario_sel]
            t.desbloquear()
            if hasattr(self, 'trabajador_dao'):
                self.trabajador_dao.guardar(t)
            if hasattr(self, 'intentos_login_dict') and usuario_sel in self.intentos_login_dict:
                self.intentos_login_dict[usuario_sel] = 0
            self.actualizar_tabla_personal()
            QMessageBox.information(self, "Éxito", f"Cuenta de '{usuario_sel}' desbloqueada exitosamente.")

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

        # Check if user is locked
        if usr in self.usuarios_sistema and self.usuarios_sistema[usr].cuenta_bloqueada:
            QMessageBox.critical(self, "Cuenta Bloqueada", "Cuenta bloqueada, contacte al administrador")
            return

        if usr in self.usuarios_sistema and self.usuarios_sistema[usr].autenticar(pwd):
            if hasattr(self, 'intentos_login_dict'):
                self.intentos_login_dict[usr] = 0
            self.usuario_actual = self.usuarios_sistema[usr]
            rol = self.usuario_actual.getRol()

            self.lbl_usuario_status.setText(f"👤 {self.usuario_actual.getNombres()} | Rol: {rol}")
            self.barras_navegacion.setVisible(True)

            # Control de Acceso por Roles (RBAC) estricto
            if rol == "Administrador":
                self.btn_socios.setVisible(True)
                self.btn_clases.setVisible(True)
                self.btn_ventas.setVisible(True)
                self.btn_personal.setVisible(True)
                self.btn_torniquete.setVisible(True)
                self.ir_a_pantalla(1)  # Ir a Socios
            elif rol == "Recepcionista":
                self.btn_socios.setVisible(True)
                self.btn_clases.setVisible(False)
                self.btn_ventas.setVisible(True)
                self.btn_personal.setVisible(False)
                self.btn_torniquete.setVisible(True)
                self.ir_a_pantalla(1)  # Ir a Socios
            elif rol == "Instructor":
                self.btn_socios.setVisible(False)
                self.btn_clases.setVisible(True)
                self.btn_ventas.setVisible(False)
                self.btn_personal.setVisible(False)
                self.btn_torniquete.setVisible(False)  # 🔒 Ocultar Torniquete al Instructor
                self.ir_a_pantalla(2)  # Ir exclusivamente a Clases Dirigidas

            self.statusBar().showMessage(f"🟢 Sesión iniciada como {self.usuario_actual.getNombres()} ({rol})")
            QMessageBox.information(self, "Acceso Concedido", f"¡Bienvenido/a {self.usuario_actual.getNombres()}!\nRol: {rol}")
        else:
            if not hasattr(self, 'intentos_login_dict'):
                self.intentos_login_dict = {}
            self.intentos_login_dict[usr] = self.intentos_login_dict.get(usr, 0) + 1
            
            if self.intentos_login_dict[usr] < 3:
                QMessageBox.warning(self, "Error de Autenticación", "Intento erroneo")
            else:
                if usr in self.usuarios_sistema:
                    u_obj = self.usuarios_sistema[usr]
                    u_obj.bloquear()
                    if hasattr(self, 'trabajador_dao'):
                        self.trabajador_dao.guardar(u_obj)
                    if hasattr(self, 'actualizar_tabla_personal'):
                        self.actualizar_tabla_personal()
                QMessageBox.critical(self, "Cuenta Bloqueada", "Cuenta bloqueada, contacte al administrador")
                return

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
        self.input_apellido_paterno = QLineEdit()
        self.input_apellido_materno = QLineEdit()
        self.input_telefono = QLineEdit()
        self.input_correo = QLineEdit()




        self.combo_estado_inicial = QComboBox()
        self.combo_estado_inicial.addItems(["🟢 Al Día (Vigente 30 días)", "🔴 Vencida / Impago (Requiere Cobro)", "⚪ Plan Cancelado / Inactivo"])

        form_socios.addRow("RUT: ", self.input_rut)
        form_socios.addRow("Nombres: ", self.input_nombres)
        form_socios.addRow("Apellido Paterno: ", self.input_apellido_paterno)
        form_socios.addRow("Apellido Materno: ", self.input_apellido_materno)
        form_socios.addRow("Teléfono: ", self.input_telefono)
        form_socios.addRow("Correo Electrónico: ", self.input_correo)
        form_socios.addRow("Estado Inicial Membresía: ", self.combo_estado_inicial)

        layout_socios.addLayout(form_socios)

        self.btn_guardar_socio = QPushButton("💾 Guardar Socio")
        self.btn_guardar_socio.setStyleSheet("background-color: #27AE60; color: white; padding: 8px; font-weight: bold;")
        self.btn_guardar_socio.clicked.connect(self.guardar_socio)
        layout_socios.addWidget(self.btn_guardar_socio)

        self.tabla_socios = QTableWidget()
        self.tabla_socios.setColumnCount(6)
        self.tabla_socios.setHorizontalHeaderLabels(["RUT", "Nombres", "Ap. Paterno", "Ap. Materno", "Teléfono", "Membresía"])
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
        apellido_pat = self.input_apellido_paterno.text().strip()
        apellido_mat = self.input_apellido_materno.text().strip()
        telefono = self.input_telefono.text().strip()

        if not rut or not nombres or not apellido_pat:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor completa al menos RUT, Nombres y Apellido Paterno")
            return

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
        try:
            nuevo_socio = Socio(
                idSocio=0,
                rut=rut,
                nombres=nombres,
                apellidoPaterno=apellido_pat, 
                apellidoMaterno=apellido_mat,
                telefono=telefono,
                correoElectronico=self.input_correo.text().strip(),
                fechaVencimientoMembresia=fecha_venc,
                estadoActivo=activo
            )
        except ValueError as ve:
            QMessageBox.critical(self, "Error de Validación", str(ve))
            return

        if isinstance(self.usuario_actual, Recepcionista):
            self.usuario_actual.registrarSocio(nuevo_socio)

        # Guardar en SQLite permanente y actualizar GUI
        self.socio_dao.guardar(nuevo_socio)
        self.socios_registrados = self.socio_dao.obtener_todos()
        self.actualizar_tabla_socios()
        self.actualizar_combo_socios_inscripcion()

        QMessageBox.information(
            self,
            "Socio Registrado",
            f"¡Socio {nombres} {apellido_pat} registrado exitosamente y guardado en SQLite!\n"
            f"Vigencia: Hasta {fecha_venc}"
        )

    def actualizar_tabla_socios(self):
        """Puebla la QTableWidget visual con los socios guardados en SQLite."""
        self.tabla_socios.setRowCount(0)
        for socio in self.socios_registrados:
            row = self.tabla_socios.rowCount()
            self.tabla_socios.insertRow(row)
            self.tabla_socios.setItem(row, 0, QTableWidgetItem(socio.rut))
            self.tabla_socios.setItem(row, 1, QTableWidgetItem(socio.nombres))
            self.tabla_socios.setItem(row, 2, QTableWidgetItem(socio.apellidoPaterno))
            self.tabla_socios.setItem(row, 3, QTableWidgetItem(socio.apellidoMaterno))
            self.tabla_socios.setItem(row, 4, QTableWidgetItem(socio.telefono))
            lbl_estado = "⚪ Plan Cancelado"
            if socio.estadoActivo:
                from src.models.excepciones import MembresiaVencidaException
                try:
                    if socio.permitirIngreso():
                        lbl_estado = "🟢 Al Día"
                except MembresiaVencidaException:
                    lbl_estado = "🔴 Vencida / Impago"
            self.tabla_socios.setItem(row, 5, QTableWidgetItem(lbl_estado))

        self.actualizar_combo_socios_inscripcion()

    def renovar_membresia_socio(self):
        items = self.tabla_socios.selectedItems()
        if not items:
            QMessageBox.warning(self, "Seleccion Requerida", "Por favor selecciona un socio en la tabla para renovar su membresía.")
            return

        row = items[0].row()
        rut_socio = self.tabla_socios.item(row, 0).text()
        socio = next((s for s in self.socios_registrados if s.rut == rut_socio), None)

        if socio: 
            #Se invoca recepcionista.cobra mensualdiad
            if isinstance(self.usuario_actual, Recepcionista):
                self.usuario_actual.cobrarMensualidad(socio, 35000)

                socio.renovarMembresia(dias=30)

                #Persistir cambio en Sqlite
                self.socio_dao.guardar(socio)
                self.actualizar_tabla_socios()

                QMessageBox.information(
                    self, 
                    "Membresia Renovada",
                    f"¡Cobro realizado! La membresía del socio {socio.nombres} {socio.apellidoPaterno} ha sido renovada en la base de datos hasta {socio.fechaVencimientoMembresia}. "

                )

    def cancelar_plan_socio(self):
        items = self.tabla_socios.selectedItems()
        if not items:
            QMessageBox.warning(self, "Selección Requerida", "Por favor selecciona un socio en la tabla para cancelar su plan.")
            return

        row = items [0].row()
        rut_socio = self.tabla_socios.item(row, 0).text()
        socio = next((s for s in self.socios_registrados if s.rut == rut_socio), None)

        if socio: 
            socio.cancelarPlan()

            #Persistir cambio en SQlite
            self.socio_dao.guardar(socio)
            self.actualizar_tabla_socios()

            QMessageBox.warning(
                self,
                "Plan Cancelado",
                f"El plan del socio {socio.nombres} ({socio.rut}) ha sido Cancelado/Desactivado en la Base de Daots. \n"
                f"El Torniquete de portería bloqueará su ingreso hasta una nueva renovación. "
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

        #Guardar en SQLIte permanentemente a través del DAO
        self.clase_dao.guardar(obj_clase)

        #Actualizar clases desde la bbdd 
        clases_list = self.clase_dao.obtener_todos()
        self.clases_registradas = {c.nombre: c for c in clases_list}
        self.clase_seleccionada_actual = self.clases_registradas.get(nombre, obj_clase)

        # Refrescar tabla visual completa
        self.actualizar_tabla_clases_bd()
        self.renderizar_mapa_sala(obj_clase)
        QMessageBox.information(self, "Clase Creada", f"¡Clase '{nombre}' ({disc}) creada en {sala} con {cupos_max} puestos!")

    def actualizar_tabla_clases_bd(self):
        """Redibuja la tabla visual de clases dirigidas con la información de SQLite."""
        if not hasattr(self, 'tabla_clases'):
            return
        self.tabla_clases.setRowCount(0)
        for obj_clase in self.clases_registradas.values():
            row = self.tabla_clases.rowCount()
            self.tabla_clases.insertRow(row)
            disc = obj_clase.__class__.__name__.replace("Clase", "")
            icono = obj_clase.obtener_icono_disciplina()
            self.tabla_clases.setItem(row, 0, QTableWidgetItem(f"{icono} {disc}"))
            self.tabla_clases.setItem(row, 1, QTableWidgetItem(obj_clase.nombre))
            self.tabla_clases.setItem(row, 2, QTableWidgetItem(f"{obj_clase.cupos_ocupados} / {obj_clase.cupo_maximo} ({obj_clase.porcentaje_ocupacion:.0f}%)"))
            self.tabla_clases.setItem(row, 3, QTableWidgetItem(obj_clase.sala))
            estado = "🔴 Llena" if obj_clase.cupos_disponibles == 0 else "🟢 Disponible"
            self.tabla_clases.setItem(row, 4, QTableWidgetItem(estado))

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
                asistio = getattr(obj_clase, 'asistencias', {}).get(pos, False)
                if asistio:
                    btn_puesto.setText(f"✔️\nPuesto {pos+1}\n{socio.getNombres()}")
                    btn_puesto.setStyleSheet(
                        "background-color: #F1C40F; color: black; font-weight: bold; border-radius: 6px; padding: 10px;"
                    )
                    btn_puesto.setToolTip(f"Asistencia CONFIRMADA: {socio.getNombres()} ({socio.getRut()})\nClic para modificar.")
                else:
                    btn_puesto.setText(f"🔴\nPuesto {pos+1}\n{socio.getNombres()}")
                    btn_puesto.setStyleSheet(
                        "background-color: #E74C3C; color: white; font-weight: bold; border-radius: 6px; padding: 10px;"
                    )
                    btn_puesto.setToolTip(f"Ocupado por: {socio.getNombres()} ({socio.getRut()})\nClic para gestionar.")
                
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
            from src.models.excepciones import MembresiaVencidaException, SinCupoException
            try:
                socio.permitirIngreso()
            except MembresiaVencidaException as e:
                QMessageBox.critical(
                    self,
                    "Acceso Denegado (Membresía Vencida)",
                    f"⛔ El socio {socio.getNombres()} ({socio.getRut()}) tiene un problema de membresía:\n\n{str(e)}\n\n"
                    f"Se debe regularizar el pago de mensualidad."
                )
                return

            # Si el usuario actual es Instructor, invocar formalmente Instructor.marcarAsistencia()
            if isinstance(self.usuario_actual, Instructor):
                asistencia_valida = self.usuario_actual.marcarAsistencia(socio, self.clase_seleccionada_actual)
                if not asistencia_valida:
                    QMessageBox.warning(self, "Asistencia Rechazada", f"No se pudo validar asistencia para {socio.getNombres()} en la clase.")
                    return

            ya_inscrito = any(s is not None and s.idSocio == socio.idSocio for s in self.clase_seleccionada_actual.cupos)
            if ya_inscrito:
                QMessageBox.warning(self, "Doble Inscripción", f"El socio {socio.getNombres()} ya está inscrito en esta clase.")
                return

            try:
                exito = self.clase_seleccionada_actual.inscribir_socio(socio, posicion)
            except SinCupoException as e:
                QMessageBox.critical(self, "Sin Cupo Físico", f"⛔ Error: {str(e)}")
                return
            if exito:
                # Guardar inscripción permanente en SQLite
                codigo_raw = str(getattr(self.clase_seleccionada_actual, 'codigo', '1'))
                id_clase_num = int(''.join(filter(str.isdigit, codigo_raw)) or '1')
                self.inscripcion_dao.inscribir_socio(socio.idSocio, id_clase_num)

                # Si es instructor, marcar asistencia en SQLite
                if isinstance(self.usuario_actual, Instructor):
                    self.inscripcion_dao.marcar_asistencia(socio.idSocio, id_clase_num, asistio=True)

                msg_autoridad = f" Asistencia validada por Instructor {self.usuario_actual.getNombres()}." if isinstance(self.usuario_actual, Instructor) else ""
                QMessageBox.information(
                    self,
                    "Reserva Exitosa",
                    f"¡{socio.getNombres()} inscrito en el Puesto {posicion+1} para {self.clase_seleccionada_actual.nombre}!{msg_autoridad}"
                )

        else:
            socio_puesto = self.clase_seleccionada_actual.cupos[posicion]
            codigo_raw = str(getattr(self.clase_seleccionada_actual, 'codigo', '1'))
            id_clase_num = int(''.join(filter(str.isdigit, codigo_raw)) or '1')
            
            if isinstance(self.usuario_actual, Instructor):
                # Flujo Instructor: Marcar/Desmarcar Asistencia
                asistio_actual = getattr(self.clase_seleccionada_actual, 'asistencias', {}).get(posicion, False)
                nuevo_estado = not asistio_actual
                accion_str = "CONFIRMAR ASISTENCIA de" if nuevo_estado else "REVOCAR ASISTENCIA de"
                
                respuesta = QMessageBox.question(
                    self,
                    "Control de Asistencia",
                    f"¿Deseas {accion_str} {socio_puesto.getNombres()}?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if respuesta == QMessageBox.Yes:
                    self.clase_seleccionada_actual.marcar_asistencia(posicion, nuevo_estado)
                    self.inscripcion_dao.marcar_asistencia(socio_puesto.idSocio, id_clase_num, asistio=nuevo_estado)
            else:
                # Flujo Admin/Recepcionista: Liberar puesto
                respuesta = QMessageBox.question(
                    self,
                    "Liberar Puesto",
                    f"¿Deseas cancelar la reserva del Puesto {posicion+1} para {socio_puesto.getNombres()}?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if respuesta == QMessageBox.Yes:
                    self.clase_seleccionada_actual.liberar_posicion(posicion)
                    self.inscripcion_dao.eliminar_inscripcion_por_relacion(socio_puesto.idSocio, id_clase_num)

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
        layout_principal_ventas = QHBoxLayout(self.vista_ventas)

        # Panel Izquierdo: Formulario de Venta y Reposición Admin
        panel_izq = QWidget()
        layout_izq = QVBoxLayout(panel_izq)

        lbl = QLabel("🛒 Punto de Venta de Suplementos & API Dólar")
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout_izq.addWidget(lbl)

        form_ventas = QFormLayout()
        self.combo_producto = QComboBox()

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

        layout_izq.addLayout(form_ventas)

        self.btn_guardar_venta = QPushButton("💳 Procesar Venta")
        self.btn_guardar_venta.setStyleSheet("background-color: #2980B9; color: white; padding: 8px; font-weight: bold;")
        self.btn_guardar_venta.clicked.connect(self.guardar_venta)
        layout_izq.addWidget(self.btn_guardar_venta)

        # Sección Administrador: Reponer Stock
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
        layout_izq.addWidget(box_admin_stock)

        # Historial de Ventas Persistido
        lbl_hist = QLabel("📄 Historial de Ventas Procesadas (Persistido en BD)")
        lbl_hist.setStyleSheet("font-weight: bold; font-size: 13px; color: #2C3E50; margin-top: 10px;")
        layout_izq.addWidget(lbl_hist)

        self.tabla_ventas = QTableWidget()
        self.tabla_ventas.setColumnCount(4)
        self.tabla_ventas.setHorizontalHeaderLabels(["Producto", "Cantidad", "Fecha / Dólar", "Total (CLP)"])
        layout_izq.addWidget(self.tabla_ventas)

        layout_principal_ventas.addWidget(panel_izq, stretch=1)

        # Panel Derecho: Inventario y Stock Físico en Tiempo Real
        panel_der = QGroupBox("📊 Inventario y Stock Físico en Tiempo Real")
        layout_der = QVBoxLayout(panel_der)

        lbl_inv_desc = QLabel("💡 Revisa el stock disponible actualizado en vivo tras cada venta o reposición:")
        lbl_inv_desc.setStyleSheet("font-size: 11px; color: #555; font-style: italic;")
        layout_der.addWidget(lbl_inv_desc)

        self.tabla_inventario = QTableWidget()
        self.tabla_inventario.setColumnCount(4)
        self.tabla_inventario.setHorizontalHeaderLabels(["ID", "Producto", "Precio USD", "Stock Disponible"])
        layout_der.addWidget(self.tabla_inventario)

        layout_principal_ventas.addWidget(panel_der, stretch=1)

        self.pantallas.addWidget(self.vista_ventas)
        self.actualizar_inventario_y_combo()
        self.cargar_historial_ventas_bd()

    def actualizar_inventario_y_combo(self):
        """Carga y refresca dinámicamente el stock en el combo y en la tabla de inventario derecha."""
        productos_defecto = [
            ("1", "Proteína Whey Gold 1kg", 45.0, 100),
            ("2", "Creatina Monohidratada 500g", 25.0, 100),
            ("3", "Pre-Entreno C4 300g", 30.0, 100),
            ("4", "BCAA Aminoácidos 400g", 20.0, 100)
        ]

        # Asegurar catálogo inicial en SQLite si no existen
        for cod, nom, pre, st in productos_defecto:
            sup_exist = self.suplemento_dao.obtener_por_id(int(cod))
            if not sup_exist:
                self.suplemento_dao.guardar(Suplemento(codigo=cod, nombre=nom, precioUSD=pre, stock=st))

        self.suplementos_bd = self.suplemento_dao.obtener_todos()

        # 1. Actualizar combo izquierdo (solo nombre de producto)
        self.combo_producto.blockSignals(True)
        self.combo_producto.clear()
        for sup in self.suplementos_bd:
            self.combo_producto.addItem(sup.nombre, sup)
        self.combo_producto.blockSignals(False)

        # 2. Actualizar tabla de inventario derecha
        self.tabla_inventario.setRowCount(0)
        for sup in self.suplementos_bd:
            r = self.tabla_inventario.rowCount()
            self.tabla_inventario.insertRow(r)
            self.tabla_inventario.setItem(r, 0, QTableWidgetItem(str(sup.codigo)))
            self.tabla_inventario.setItem(r, 1, QTableWidgetItem(sup.nombre))
            self.tabla_inventario.setItem(r, 2, QTableWidgetItem(f"${sup.precioUSD:.2f} USD"))
            
            lbl_stock = f"📦 {sup.stock} unidades"
            item_st = QTableWidgetItem(lbl_stock)
            if sup.stock <= 5:
                item_st.setForeground(Qt.red)
            self.tabla_inventario.setItem(r, 3, item_st)

    def al_cambiar_producto_venta(self):
        """Mantiene sincronizada la selección actual del producto."""
        pass

    def reponer_stock_admin(self):
        admin_autoridad = self.usuario_actual if isinstance(self.usuario_actual, Administrador) else self.usuarios_sistema.get("admin")
        if not admin_autoridad or not isinstance(admin_autoridad, Administrador):
            QMessageBox.warning(self, "Acceso Denegado", "Solo el Administrador posee permisos para reponer stock físico.")
            return

        cant_str = self.input_reponer_cant.text().strip()
        try:
            cant = int(cant_str)
        except ValueError:
            QMessageBox.warning(self, "Valor Inválido", "La cantidad a reponer debe ser un número entero.")
            return

        obj_suplemento = self.combo_producto.currentData()
        if not obj_suplemento:
            QMessageBox.warning(self, "Selección Inválida", "Por favor selecciona un producto válido de la lista.")
            return

        # Invocar Administrador.reponerStock(sup, cant)
        admin_autoridad.reponerStock(obj_suplemento, cant)
        self.suplemento_dao.guardar(obj_suplemento)

        # Refrescar productos en la UI y la tabla de inventario derecha
        self.actualizar_inventario_y_combo()

        QMessageBox.information(
            self,
            "Stock Repuesto",
            f"¡El Administrador {admin_autoridad.getNombres()} ha repuesto +{cant} unidades de '{obj_suplemento.nombre}' en SQLite!\n"
            f"Nuevo Stock Total: {obj_suplemento.stock} unidades."
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

        obj_suplemento = self.combo_producto.currentData()
        if not obj_suplemento:
            idx = self.combo_producto.currentIndex()
            if hasattr(self, 'suplementos_bd') and idx >= 0 and idx < len(self.suplementos_bd):
                obj_suplemento = self.suplementos_bd[idx]

        if not obj_suplemento:
            QMessageBox.warning(self, "Producto Inválido", "No se encontró el producto seleccionado.")
            return

        # Reconsultar el suplemento fresco desde SQLite para asegurar sincronía 100% real
        id_sup_num = int(obj_suplemento.codigo) if str(obj_suplemento.codigo).isdigit() else 1
        sup_actualizado = self.suplemento_dao.obtener_por_id(id_sup_num)
        if sup_actualizado:
            obj_suplemento = sup_actualizado

        # 2. Verificar Stock (Regla #6 UML) sobre la información más fresca de la BD
        if not obj_suplemento.hayStock(cant):
            QMessageBox.warning(self, "Stock Insuficiente", f"No hay stock suficiente para {obj_suplemento.nombre} (Stock actual: {obj_suplemento.stock}).")
            return

        precio_clp = obj_suplemento.calcularPrecioCLP(valor_dolar)



        # 3. Crear DetalleVenta y Venta compuesta (UML)
        obj_detalle = DetalleVenta(cantidad=cant, precioUnitarioCLP=precio_clp, suplemento=obj_suplemento)
        obj_venta = Venta(numero=self.tabla_ventas.rowCount() + 1)
        exito = obj_venta.agregarDetalle(obj_detalle)

        # 4. Invocar Recepcionista.registrarVenta(venta) si corresponde (UML)
        recepcion_autoridad = self.usuario_actual if isinstance(self.usuario_actual, Recepcionista) else self.usuarios_sistema.get("recepcion")
        if recepcion_autoridad and hasattr(recepcion_autoridad, 'registrarVenta'):
            recepcion_autoridad.registrarVenta(obj_venta)

        # 5. Persistir Venta en SQLite permanentemente a través de VentaDAO
        if hasattr(self, 'venta_dao'):
            self.venta_dao.guardar(obj_venta)

        self.cargar_historial_ventas_bd()

        # Refrescar vista del combo guardando el indice
        idx_previo = self.combo_producto.currentIndex()
        self.actualizar_inventario_y_combo()
        if idx_previo >= 0 and idx_previo < self.combo_producto.count():
            self.combo_producto.setCurrentIndex(idx_previo)

        if not exito:
            QMessageBox.warning(self, "Error", "No se pudo agregar el detalle de venta (Posible falta de stock local).")
            return

        QMessageBox.information(
            self,
            "Venta Transaccional Procesada",
            f"¡Venta N° {obj_venta.numero} de '{obj_suplemento.nombre}' procesada con éxito y guardada en BD!\n"
            f"💰 Total CLP: ${obj_venta.totalCLP:,.0f}\n"
            f"📦 Stock Restante en BD: {obj_suplemento.stock} unidades"
        )

    def cargar_historial_ventas_bd(self):
        """Carga y muestra el historial de ventas procesadas desde la base de datos SQLite."""
        if not hasattr(self, 'venta_dao'):
            return
        ventas_bd = self.venta_dao.obtener_todos()
        self.tabla_ventas.setRowCount(0)
        for v in ventas_bd:
            r = self.tabla_ventas.rowCount()
            self.tabla_ventas.insertRow(r)
            self.tabla_ventas.setItem(r, 0, QTableWidgetItem(str(v.get('nombre_producto', 'Suplemento'))))
            self.tabla_ventas.setItem(r, 1, QTableWidgetItem(f"{v.get('cantidad', 1)} un."))
            self.tabla_ventas.setItem(r, 2, QTableWidgetItem(str(v.get('fecha', 'N/A'))))
            self.tabla_ventas.setItem(r, 3, QTableWidgetItem(f"${v.get('total_clp', 0.0):,.0f} CLP"))

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
        self.input_trab_apellido_pat = QLineEdit()
        self.input_trab_apellido_mat = QLineEdit()
        self.input_trab_usuario = QLineEdit()
        self.input_trab_pass = QLineEdit()
        self.input_trab_pass.setEchoMode(QLineEdit.Password)

        self.combo_trab_rol = QComboBox()
        self.combo_trab_rol.addItems(["Recepcionista", "Instructor", "Administrador"])

        form_personal.addRow("Rol a Asignar: ", self.combo_trab_rol)
        form_personal.addRow("RUT: ", self.input_trab_rut)
        form_personal.addRow("Nombres: ", self.input_trab_nombres)
        form_personal.addRow("Apellido Paterno: ", self.input_trab_apellido_pat)
        form_personal.addRow("Apellido Materno: ", self.input_trab_apellido_mat)
        form_personal.addRow("Nombre Usuario: ", self.input_trab_usuario)
        form_personal.addRow("Contraseña: ", self.input_trab_pass)

        layout_personal.addLayout(form_personal)

        self.btn_guardar_trabajador = QPushButton("➕ Crear Trabajador (Invoca Admin.crearTrabajador)")
        self.btn_guardar_trabajador.setStyleSheet("background-color: #8E44AD; color: white; padding: 10px; font-weight: bold;")
        self.btn_guardar_trabajador.clicked.connect(self.guardar_trabajador_admin)
        layout_personal.addWidget(self.btn_guardar_trabajador)

        self.tabla_personal = QTableWidget()
        self.tabla_personal.setColumnCount(5)
        self.tabla_personal.setHorizontalHeaderLabels(["ID", "Usuario", "Nombre Completo", "Rol", "Estado"])
        layout_personal.addWidget(self.tabla_personal)

        self.btn_desbloquear_trabajador = QPushButton("🔓 Desbloquear Trabajador")
        self.btn_desbloquear_trabajador.setStyleSheet("background-color: #27AE60; color: white; padding: 10px; font-weight: bold;")
        self.btn_desbloquear_trabajador.clicked.connect(self.desbloquear_trabajador_admin)
        layout_personal.addWidget(self.btn_desbloquear_trabajador)

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
        admin_autoridad = self.usuario_actual if isinstance(self.usuario_actual, Administrador) else self.usuarios_sistema.get("admin")
        
        if not admin_autoridad or not isinstance(admin_autoridad, Administrador):
            QMessageBox.warning(
                self,
                "Acceso Denegado (Requiere Administrador)",
                "Para registrar personal debes haber iniciado sesión como Administrador (Usuario: admin / Contraseña: admin123)."
            )
            return

        rol = self.combo_trab_rol.currentText()
        rut = self.input_trab_rut.text().strip()
        nombres = self.input_trab_nombres.text().strip()
        apellido_pat = self.input_trab_apellido_pat.text().strip()
        apellido_mat = self.input_trab_apellido_mat.text().strip()
        usr = self.input_trab_usuario.text().strip()
        pwd = self.input_trab_pass.text().strip()

        if not rut or not nombres or not usr or not pwd:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor completa RUT, Nombres, Usuario y Contraseña.")
            return

        nuevo_id = "0"
        if rol == "Recepcionista":
            nuevo_t = Recepcionista(
                idTrabajador=nuevo_id, rut=rut, nombres=nombres, apellidoPaterno=apellido_pat, apellidoMaterno=apellido_mat, usuario=usr, passHash=pwd
            )
        elif rol == "Instructor":
            nuevo_t = Instructor(
                especialidad="Fitness", idTrabajador=nuevo_id, rut=rut, nombres=nombres, apellidoPaterno=apellido_pat, apellidoMaterno=apellido_mat, usuario=usr, passHash=pwd
            )
        else:
            nuevo_t = Administrador(
                nivelAcceso="General", idTrabajador=nuevo_id, rut=rut, nombres=nombres, apellidoPaterno=apellido_pat, apellidoMaterno=apellido_mat, usuario=usr, passHash=pwd
            )

        try:
            # Invocar formalmente Administrador.crearTrabajador(t)
            exito = admin_autoridad.crearTrabajador(nuevo_t)
            if exito:
                # Guardar en SQLite permanente
                self.trabajador_dao.guardar(nuevo_t)

                # Releer de SQLite para obtener los objetos actualizados con IDs reales
                trabajadores_bd = self.trabajador_dao.obtener_todos()
                for t in trabajadores_bd:
                    key_u = getattr(t, 'usuario', None) or t.nombres.lower().replace(" ", "")
                    self.usuarios_sistema[key_u] = t

                # Refrescar tabla visual de personal
                self.actualizar_tabla_personal()

                # Limpiar entradas de texto
                self.input_trab_rut.clear()
                self.input_trab_nombres.clear()
                self.input_trab_apellido_pat.clear()
                self.input_trab_apellido_mat.clear()
                self.input_trab_usuario.clear()
                self.input_trab_pass.clear()

                QMessageBox.information(
                    self,
                    "Trabajador Creado",
                    f"¡El Administrador {admin_autoridad.getNombres()} ha creado al trabajador {nombres} con rol {rol} en la Base de Datos!"
                )
        except Exception as err:
            QMessageBox.critical(
                self,
                "Error al Guardar Trabajador",
                f"No se pudo guardar el trabajador en la base de datos:\n{str(err)}"
            )

    def actualizar_tabla_personal(self):
        """Redibuja la tabla visual de personal con los usuarios registrados en el sistema."""
        self.tabla_personal.setRowCount(0)
        for u in self.usuarios_sistema.values():
            r = self.tabla_personal.rowCount()
            self.tabla_personal.insertRow(r)
            self.tabla_personal.setItem(r, 0, QTableWidgetItem(str(u.idTrabajador)))
            self.tabla_personal.setItem(r, 1, QTableWidgetItem(u.usuario))
            self.tabla_personal.setItem(r, 2, QTableWidgetItem(f"{u.nombres} {u.apellidoPaterno}"))
            self.tabla_personal.setItem(r, 3, QTableWidgetItem(u.getRol()))
            estado = "Bloqueado 🔴" if u.cuenta_bloqueada else "Activo"
            self.tabla_personal.setItem(r, 4, QTableWidgetItem(estado))




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
        from src.models.excepciones import MembresiaVencidaException
        try:
            permitido = socio.permitirIngreso()
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
        except MembresiaVencidaException as e:
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