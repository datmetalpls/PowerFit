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
)
from PySide6.QtCore import Qt

from src.models import (
    Persona,
    Direccion,
    cargar_comunas_ine,
    Trabajador,
    Instructor,
    Recepcionista,
    Socio,
)


class VentanaPrincipalPowerFit(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PowerFit - Sistema de Gestión de Gimnasio")
        self.resize(850, 650)
        self.setStyleSheet("background-color: #F4F6F7;")

        # Usuario autenticado actualmente
        self.usuario_actual = None

        # Base de datos simulada de usuarios del sistema (RBAC)
        self.usuarios_sistema = {
            "admin": Trabajador(
                idTrabajador=1,
                usuario="admin",
                passHash="admin123",
                rol="Administrador",
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

        # Layout Principal
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.layout_principal = QVBoxLayout(self.widget_central)

        # 1. Barra superior de navegación (inicialmente oculta antes del Login)
        self.barras_navegacion = QWidget()
        layout_nav = QHBoxLayout(self.barras_navegacion)

        self.lbl_usuario_status = QLabel("👤 No autenticado")
        self.lbl_usuario_status.setStyleSheet("font-weight: bold; color: #2C3E50;")

        self.btn_socios = QPushButton("👤 Gestión de Socios")
        self.btn_clases = QPushButton("🏋️ Clases Dirigidas")
        self.btn_ventas = QPushButton("🛒 Punto de Venta (Dólar)")
        self.btn_logout = QPushButton("🔴 Cerrar Sesión")

        estilo_btn_nav = "background-color: #34495E; color: white; padding: 8px; font-weight: bold;"
        self.btn_socios.setStyleSheet(estilo_btn_nav)
        self.btn_clases.setStyleSheet(estilo_btn_nav)
        self.btn_ventas.setStyleSheet(estilo_btn_nav)
        self.btn_logout.setStyleSheet("background-color: #C0392B; color: white; padding: 8px; font-weight: bold;")

        layout_nav.addWidget(self.lbl_usuario_status)
        layout_nav.addStretch()
        layout_nav.addWidget(self.btn_socios)
        layout_nav.addWidget(self.btn_clases)
        layout_nav.addWidget(self.btn_ventas)
        layout_nav.addWidget(self.btn_logout)

        self.layout_principal.addWidget(self.barras_navegacion)
        self.barras_navegacion.setVisible(False)

        # 2. Pila de Pantallas (QStackedWidget)
        self.pantallas = QStackedWidget()

        # Vistas de la aplicación
        self.construir_vista_login()    # Índice 0
        self.construir_vista_socios()   # Índice 1
        self.construir_vista_clases()   # Índice 2
        self.construir_vista_ventas()   # Índice 3

        self.layout_principal.addWidget(self.pantallas)

        # Conectar eventos de botones de navegación
        self.btn_socios.clicked.connect(lambda: self.pantallas.setCurrentIndex(1))
        self.btn_clases.clicked.connect(lambda: self.pantallas.setCurrentIndex(2))
        self.btn_ventas.clicked.connect(lambda: self.pantallas.setCurrentIndex(3))
        self.btn_logout.clicked.connect(self.cerrar_sesion)

        self.statusBar().showMessage("🔒 Por favor inicie sesión para acceder al sistema.")

    # =========================================================================
    # VISTA 0: LOGIN & AUTENTICACIÓN RBAC
    # =========================================================================
    def construir_vista_login(self):
        self.vista_login = QWidget()
        layout = QVBoxLayout(self.vista_login)
        layout.setAlignment(Qt.AlignCenter)

        # Tarjeta de Login
        card = QWidget()
        card.setFixedSize(400, 360)
        card.setStyleSheet("background-color: white; border-radius: 10px; border: 1px solid #BDC3C7;")
        layout_card = QVBoxLayout(card)

        lbl_titulo = QLabel("🏋️ PowerFit Gym")
        lbl_subtitulo = QLabel("Autenticación & Control de Acceso (RBAC)")
        lbl_titulo.setAlignment(Qt.AlignCenter)
        lbl_subtitulo.setAlignment(Qt.AlignCenter)
        lbl_titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #2C3E50;")
        lbl_subtitulo.setStyleSheet("font-size: 12px; color: #7F8C8D;")

        form = QFormLayout()
        self.input_login_usuario = QLineEdit()
        self.input_login_password = QLineEdit()
        self.input_login_password.setEchoMode(QLineEdit.Password)

        self.input_login_usuario.setPlaceholderText("Ej: admin, recepcion, instructor")
        self.input_login_password.setPlaceholderText("Contraseña")

        form.addRow("Usuario:", self.input_login_usuario)
        form.addRow("Contraseña:", self.input_login_password)

        btn_ingresar = QPushButton("🔑 Iniciar Sesión")
        btn_ingresar.setStyleSheet("background-color: #27AE60; color: white; padding: 10px; font-size: 14px; font-weight: bold;")
        btn_ingresar.clicked.connect(self.iniciar_sesion)

        # Ayuda de credenciales demo
        lbl_demo = QLabel(
            "💡 <b>Cuentas de Prueba:</b><br>"
            "• Admin: <code>admin</code> / <code>admin123</code><br>"
            "• Recepción: <code>recepcion</code> / <code>rec123</code><br>"
            "• Instructor: <code>instructor</code> / <code>ins123</code>"
        )
        lbl_demo.setStyleSheet("font-size: 11px; color: #555; background-color: #EAECEE; padding: 6px; border-radius: 5px;")

        layout_card.addWidget(lbl_titulo)
        layout_card.addWidget(lbl_subtitulo)
        layout_card.addSpacing(10)
        layout_card.addLayout(form)
        layout_card.addSpacing(10)
        layout_card.addWidget(btn_ingresar)
        layout_card.addSpacing(10)
        layout_card.addWidget(lbl_demo)

        layout.addWidget(card)
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
                self.pantallas.setCurrentIndex(1)  # Ir a Socios
            elif rol == "Recepcionista":
                self.btn_socios.setVisible(True)
                self.btn_clases.setVisible(False)
                self.btn_ventas.setVisible(True)
                self.pantallas.setCurrentIndex(1)  # Ir a Socios
            elif rol == "Instructor":
                self.btn_socios.setVisible(False)
                self.btn_clases.setVisible(True)
                self.btn_ventas.setVisible(False)
                self.pantallas.setCurrentIndex(2)  # Ir a Clases

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

        form_socios.addRow("RUT: ", self.input_rut)
        form_socios.addRow("Nombres: ", self.input_nombres)
        form_socios.addRow("Apellidos: ", self.input_apellidos)
        form_socios.addRow("Teléfono: ", self.input_telefono)
        form_socios.addRow("Correo Electrónico: ", self.input_correo)
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
        self.tabla_socios.setColumnCount(5)
        self.tabla_socios.setHorizontalHeaderLabels(["RUT", "Nombre Completo", "Teléfono", "Comuna", "Vivienda"])
        layout_socios.addWidget(self.tabla_socios)

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

        QMessageBox.information(self, "Socio Registrado", f"¡Socio {nombres} {apellidos} registrado exitosamente!")

    # =========================================================================
    # VISTA 2: CLASES DIRIGIDAS
    # =========================================================================
    def construir_vista_clases(self):
        self.vista_clases = QWidget()
        layout_clases = QVBoxLayout(self.vista_clases)

        lbl = QLabel("🏋️ Clases Dirigidas (Yoga, Spinning, Crossfit)")
        lbl.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
        layout_clases.addWidget(lbl)

        form_clases = QFormLayout()
        self.combo_disciplina = QComboBox()
        self.combo_disciplina.addItems(["Yoga", "Spinning", "Crossfit"])

        self.input_nombre_clase = QLineEdit()
        self.input_cupo_maximo = QLineEdit()
        self.input_duracion = QLineEdit()
        self.input_detalle_especifico = QLineEdit()

        form_clases.addRow("Disciplina: ", self.combo_disciplina)
        form_clases.addRow("Nombre de la Clase: ", self.input_nombre_clase)
        form_clases.addRow("Cupo Máximo: ", self.input_cupo_maximo)
        form_clases.addRow("Duración (minutos): ", self.input_duracion)
        form_clases.addRow("Detalle Específico: ", self.input_detalle_especifico)

        layout_clases.addLayout(form_clases)

        self.btn_guardar_clase = QPushButton("📌 Registrar Clase")
        self.btn_guardar_clase.setStyleSheet("background-color: #D35400; color: white; padding: 8px; font-weight: bold;")
        self.btn_guardar_clase.clicked.connect(self.guardar_clase)
        layout_clases.addWidget(self.btn_guardar_clase)

        self.tabla_clases = QTableWidget()
        self.tabla_clases.setColumnCount(5)
        self.tabla_clases.setHorizontalHeaderLabels(["Disciplina", "Nombre", "Cupos", "Duración", "Detalle"])
        layout_clases.addWidget(self.tabla_clases)

        self.pantallas.addWidget(self.vista_clases)

    def guardar_clase(self):
        disc = self.combo_disciplina.currentText()
        nombre = self.input_nombre_clase.text().strip()
        cupos = self.input_cupo_maximo.text().strip()
        duracion = self.input_duracion.text().strip()
        detalle = self.input_detalle_especifico.text().strip()

        if not nombre or not cupos:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor ingresa Nombre y Cupos de la clase.")
            return

        row = self.tabla_clases.rowCount()
        self.tabla_clases.insertRow(row)
        self.tabla_clases.setItem(row, 0, QTableWidgetItem(disc))
        self.tabla_clases.setItem(row, 1, QTableWidgetItem(nombre))
        self.tabla_clases.setItem(row, 2, QTableWidgetItem(cupos))
        self.tabla_clases.setItem(row, 3, QTableWidgetItem(f"{duracion} min"))
        self.tabla_clases.setItem(row, 4, QTableWidgetItem(detalle))

        QMessageBox.information(self, "Clase Registrada", f"¡Clase '{nombre}' ({disc}) registrada con éxito!")

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

        self.tabla_ventas = QTableWidget()
        self.tabla_ventas.setColumnCount(4)
        self.tabla_ventas.setHorizontalHeaderLabels(["Producto", "Cantidad", "Valor Dólar", "Total Estimado (CLP)"])
        layout_ventas.addWidget(self.tabla_ventas)

        self.pantallas.addWidget(self.vista_ventas)

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
        cant = self.input_cantidad.text().strip()
        dolar_clp = self.input_valor_dolar.text().strip()

        if not cant or not dolar_clp:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor ingresa cantidad y valor del dólar en CLP.")
            return

        precio_usd = 45 if "Whey" in prod else (25 if "Creatina" in prod else (30 if "Pre-Entreno" in prod else 20))
        total_clp = float(cant) * precio_usd * float(dolar_clp)

        row = self.tabla_ventas.rowCount()
        self.tabla_ventas.insertRow(row)
        self.tabla_ventas.setItem(row, 0, QTableWidgetItem(prod))
        self.tabla_ventas.setItem(row, 1, QTableWidgetItem(cant))
        self.tabla_ventas.setItem(row, 2, QTableWidgetItem(f"${dolar_clp} CLP"))
        self.tabla_ventas.setItem(row, 3, QTableWidgetItem(f"${total_clp:,.0f} CLP"))

        QMessageBox.information(self, "Venta Procesada", f"¡Venta de '{prod}' procesada por un total de ${total_clp:,.0f} CLP!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipalPowerFit()
    ventana.show()
    sys.exit(app.exec())