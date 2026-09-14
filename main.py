"""PowerFit - Punto de entrada principal."""

import sys
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
)
from src.models import Persona, Direccion, cargar_comunas_ine
from PySide6.QtCore import Qt
import uuid

class VentanaPrincipalPowerFit(QMainWindow):

        def guardar_socio(self):

            #1. extraer los datos de la interfazo gráfica 

            rut = self.input_rut.text().strip()
            nombres = self.input_nombres.text().strip()
            apellidos = self.input_apellidos.text().strip()
            telefono = self.input_telefono.text().strip()
            correo = self.input_correo.text().strip()
            tipo_direccion = self.combo_tipo_direccion.currentText()
            calle = self.input_calle.text().strip()
            numero = self.input_numero.text().strip()
            referencia = self.input_referencia.text().strip()
            comuna = self.combo_comunas.currentText()

            #2. validar que no haya campos vacíos básicos 
            if not rut or not nombres or not apellidos: 
                 QMessageBox.warning(self, "Campos Incompletos", "Por favor completa al menos RUT, Nombres y Apellidos")
                 return

            #3. Mostrar ventana emergente de confirmación exitosa
            QMessageBox.information(
                 self,
                 "Socio Registrado",
                 f"¡Socio registrado con éxito!\n\n"
                 f"RUT: {rut}\n"
                 f"Nombre: {nombres} {apellidos}\n"
                 f"Direccion: {calle}  {numero}  {tipo_direccion} ({comuna})"
            )

            #actualziar el mensaje de la barra de estado 
            self.statusBar().showMessage(f"Último socio registrado: {nombres} {apellidos} ({rut})")

        def __init__(self):
             super().__init__()

             #1. Configuración del Marco (título y tamaño)
             self.setWindowTitle("Powerfit - Sistema de gestión de Gimnasio")
             self.resize(800,600)

             #2 Crear el contenedor central y su organizador (layout)
             contenedor_central = QWidget()
             self.setCentralWidget(contenedor_central)

             layout_principal=QVBoxLayout()
             contenedor_central.setLayout(layout_principal)

             #3. Agregar un título de bienvenido
             lbl_bienvenida=QLabel("Bienvenido a Powerfit")
             lbl_bienvenida.setStyleSheet("font-size: 24px; font-weight: bold; color: #2C3E50")
             lbl_bienvenida.setAlignment(Qt.AlignCenter)
             layout_principal.addWidget(lbl_bienvenida)

             #4. Crear un organizador Horizontal para los botones del menú. 
             layout_botones = QHBoxLayout()

             #Crear los tres botones principales
             self.btn_socios = QPushButton("🏋️ Gestión de Socios") 
             self.btn_clases = QPushButton("🧘 Clases Dirigidas")
             self.btn_ventas = QPushButton("🛒 Ventas e Inventario")

             #se agregan al layout
             layout_botones.addWidget(self.btn_socios)
             layout_botones.addWidget(self.btn_clases)
             layout_botones.addWidget(self.btn_ventas)

             # Finalmente meter toda la fila de botones DENTRO del layout principal vertical 
             layout_principal.addLayout(layout_botones)

             #5 crear la barra de estado inferior
             self.statusBar().showMessage("Sistema PowerFit iniciado correctamente")             
             estilo_botones= """
                QPushButton {
                background-color: #34495E;
                color: White;
                font-size: 14px;
                padding: 10px;
                border-radius: 5px;
                }

                QPushButton:hover{
                background-color: #298089}
             """

             self.btn_socios.setStyleSheet(estilo_botones)
             self.btn_clases.setStyleSheet(estilo_botones)
             self.btn_ventas.setStyleSheet(estilo_botones)

             #crear el contenedor apilado en pantallas (QStackedWidget)
             self.pantallas = QStackedWidget()

             #Pantalla 1 : gestión de socios
             self.vista_socios=QWidget()
             layout_socios=QVBoxLayout()
             self.vista_socios.setLayout(layout_socios)

             #Subtitulo de la sección
             lbl_titulo_socios = QLabel("📋 Registro de Nuevo Socio")
             lbl_titulo_socios.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")

             layout_socios.addWidget(lbl_titulo_socios)

             #crear formulario de QFormLayout
             formulario = QFormLayout()

             #Crear los campos de entrada (loh inputs)
             self.input_rut = QLineEdit()
             self.input_rut.setPlaceholderText("Ej: 12345678-9")

             self.input_nombres = QLineEdit()
             self.input_nombres.setPlaceholderText("Nombres del socio")

             self.input_apellidos = QLineEdit()
             self.input_apellidos.setPlaceholderText("Apellido paterno y materno")

             self.input_telefono = QLineEdit()
             self.input_telefono.setPlaceholderText("+56 9 1234 5678")

             self.input_correo = QLineEdit()
             self.input_correo.setPlaceholderText("socio@ejemplo.com")

             #---Campos de direccion
             self.combo_tipo_direccion = QComboBox()
             self.combo_tipo_direccion.addItems (["Casa", "Departamento", "Block"])

             self.input_calle = QLineEdit()
             self.input_calle.setPlaceholderText("Nombre de la calle: ")

             self.input_numero = QLineEdit()
             self.input_numero.setPlaceholderText("Ej: 1234")

             self.input_referencia = QLineEdit()
             self.input_referencia.setPlaceholderText("Ej: Esquina Los Leones")

             #Agregar las filas al formulario --- eq

             #desplegable de comunas

             #cargar catálogo real de las 346 comnas de chilito
             diccionario_comunas = cargar_comunas_ine()
             nombres_comunas = [c.nombre for c in diccionario_comunas.values()]

             self.combo_comunas = QComboBox()
             self.combo_comunas.addItems(nombres_comunas) 

             #agregar cada fila al formulario (etiqueta, campo)
             formulario.addRow("Rut: ", self.input_rut)
             formulario.addRow("Nombres: ", self.input_nombres)
             formulario.addRow("Apellidos: ",self.input_apellidos)
             formulario.addRow("Teléfono: ", self.input_telefono)
             formulario.addRow("Correo electrónico: ", self.input_correo)
             formulario.addRow("Tipo vivienda: ", self.combo_tipo_direccion)
             formulario.addRow("Calle: ", self.input_calle)
             formulario.addRow("Número: ", self.input_numero)
             formulario.addRow("Referencia: ", self.input_referencia)
             formulario.addRow("Comuna: ", self.combo_comunas)

             #agregar el formulario al layout de la vista de socios
             layout_socios.addLayout(formulario)

             #botón de guardar socio
             self.btn_guardar_socio = QPushButton ("💾 Guardar Socio")
             self.btn_guardar_socio.setStyleSheet("background-color: #27AE60; color: white;  padding: 8px; font-weight: bold;")

             layout_socios.addWidget(self.btn_guardar_socio)
             self.btn_guardar_socio.clicked.connect(self.guardar_socio)
         

             self.vista_clases = QLabel("🧘 Pantalla de Clases Dirigidas")
             self.vista_clases.setAlignment(Qt.AlignCenter)

             self.vista_ventas = QLabel ("🛒 Pantalla de Ventas e Inventario")
             self.vista_ventas.setAlignment(Qt.AlignCenter)

             #Agregar las 3 vistas a la pila de pantallas (índices.0 1 y 2)
             self.pantallas.addWidget(self.vista_socios) #index 0
             self.pantallas.addWidget(self.vista_clases) #index 1
             self.pantallas.addWidget(self.vista_clases) #index 2

             #agregar el QStacked Widget al layout principal
             layout_principal.addWidget(self.pantallas)

             #7 conecta los clics de los botones con el cabio de pantalla
             self.btn_socios.clicked.connect(lambda: self.pantallas.setCurrentIndex(0))
             self.btn_clases.clicked.connect(lambda: self.pantallas.setCurrentIndex(1))
             self.btn_ventas.clicked.connect(lambda: self.pantallas.setCurrentIndex(2))

             


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 1. Crear la app
    ventana = VentanaPrincipalPowerFit()   # 2. Crear tu ventana POO
    ventana.show()                # 3. Mostrarla en pantalla
    sys.exit(app.exec())          # 4. Iniciar bucle de eventos





Usuario=Persona("2111111-K", "César", "Guerrero", "Acevedo", "+56333434342", "correo@notiene.cl")
comu_ine=cargar_comunas_ine()

print(Usuario.getRut())
print(Usuario.getNombres())

id_autogenerado=str(uuid.uuid4())
domicilio=Direccion(id_autogenerado, "Casa", "Ramon Venegas", 3116, "El parque")

print("ID: ", domicilio.getIdDireccion(), "\n", "Calle:", domicilio.getCalle(), "\n", "Número: ", domicilio.getNumero(), "\n", "Calle Referencia: ", domicilio.getReferencia(), "\n", "Comuna: ", comu_ine.get(13101).nombre)