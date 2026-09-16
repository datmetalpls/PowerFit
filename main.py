"""PowerFit - Punto de entrada principal."""
import os
import sys
import PySide6

# Asegurar la ruta de plugins de Qt (soluciona error cocoa en macOS/entornos virtuales)
pyside_dir = os.path.dirname(PySide6.__file__)
plugins_dir = os.path.join(pyside_dir, "Qt", "plugins")
if os.path.exists(plugins_dir):
    os.environ["QT_PLUGIN_PATH"] = plugins_dir

import json
import urllib.request
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
                 f"Teléfono:  {telefono} | correo: {correo}\n"
                 f"Direccion: {calle}  {numero}  {tipo_direccion} ({comuna})"
                 f"Referencia: {referencia}"
            )

            #actualziar el mensaje de la barra de estado 
            self.statusBar().showMessage(f"Último socio registrado: {nombres} {apellidos} ({rut})")
            #agregar uan nueva fila a la tabla visual de socios
            fila=self.tabla_socios.rowCount()
            self.tabla_socios.insertRow(fila)
            self.tabla_socios.setItem(fila, 0,QTableWidgetItem(rut))
            self.tabla_socios.setItem(fila, 1,QTableWidgetItem(f"{nombres} {apellidos}"))
            self.tabla_socios.setItem(fila, 2,QTableWidgetItem(telefono))
            self.tabla_socios.setItem(fila, 3,QTableWidgetItem(comuna))
            self.tabla_socios.setItem(fila, 4,QTableWidgetItem(tipo_direccion))

        def guardar_clase(self):
             #extrar datos de lai interfaz

             disciplina = self.combo_tipo_clase.currentText()
             nombre = self.input_nombre_clase.text().strip()
             cupo = self.input_cupo_maximo.text().strip()
             duracion=self.input_duracion.text().strip()
             detalle = self.input_especifico_clase.text().strip()

             #validar campos vacíos :V
             if not nombre or not cupo or not duracion: 
                  QMessageBox.warning(self, "Campos Incompletos", "Por favor completa Nombre, Cupo y Duración.")
                  return

             #ventana emergente de confirmación 
             QMessageBox.information(
                  self,
                  "Clase Creada", 
                  f"¡Clase Dirigida creada con éxito! \n \n"
                  f"Disciplina: {disciplina}\n"
                  f"Nombre: {nombre}\n"
                  f"Cupo Máximo: {cupo} socios \n"
                  f"Duración: {duracion} min \n"
                  f"Detalle: {detalle}"
             )

             #4. Actualizar la barra de estado 
             self.statusBar().showMessage(f"Últma clase registrada: {nombre} ({disciplina})")

             fila=self.tabla_clases.rowCount()
             self.tabla_clases.insertRow(fila)
             self.tabla_clases.setItem(fila, 0, QTableWidgetItem(disciplina))
             self.tabla_clases.setItem(fila, 1, QTableWidgetItem(nombre))
             self.tabla_clases.setItem(fila, 2, QTableWidgetItem(cupo))
             self.tabla_clases.setItem(fila, 3, QTableWidgetItem(duracion))
             self.tabla_clases.setItem(fila, 4, QTableWidgetItem(detalle))

        def guardar_venta(self):
             producto = self.combo_producto.currentText()
             cantidad = self.input_cantidad.text().strip()
             valor_dolar = self.input_valor_dolar.text().strip()

             if not cantidad or not valor_dolar: 
                  QMessageBox.warning(self, "Campos incomletos", "Por favor ingresa Cantidad y Valor del Dólar.")
                  return
             
             QMessageBox.information (
                 self, 
                 "Venta procesada",
                 f"?Venta registrda con éxito! \n \n"
                 f"Producto: {producto} \n"
                 f"Cantidad: {cantidad}\n"
                 f"Tasa Dólar: ${valor_dolar} CLP "

            )
             self.statusBar().showMessage(f"última venta relizada: {cantidad} x {producto}")

             #Calcular estimado en CLP
             try: 
                  total_clp = int (cantidad) * float(valor_dolar)
                  texto_total = f"${total_clp:,.0f} CLP"
             except ValueError:
                texto_total = "N/A"

            #Agregar fila a la tabla de ventas
             fila = self.tabla_ventas.rowCount()
             self.tabla_ventas.insertRow(fila)
             self.tabla_ventas.setItem(fila, 0, QTableWidgetItem(producto))
             self.tabla_ventas.setItem(fila, 1, QTableWidgetItem(cantidad))
             self.tabla_ventas.setItem(fila, 2, QTableWidgetItem(f"${valor_dolar} CLP"))
             self.tabla_ventas.setItem(fila, 3, QTableWidgetItem(texto_total))
        


        def cargar_dolar_api(self):
             self.statusBar().showMessage("Consultando API de mindicador.cl....")
             url= "https://mindicador.cl/api/dolar"
             try: 
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as responde:
                    datos = json.loads(responde.read().decode())
                    valor = datos["serie"][0]["valor"]
                    self.input_valor_dolar.setText(str(valor))
                    self.statusBar().showMessage(f"Dólar oficial en vivo: ${valor} CLP")
                    QMessageBox.information(self, "API Dólar Oficial", f"¡Dólar del día cargado exitosamente! \nValor oficial: ${valor} CLP")
             except Exception as err:
               self.statusBar().showMessage("Error al consultar API del dólar")
               QMessageBox.warning(self,"Error de conexión", f"No se pudo consultar la API. Ingresa el valor manualmente. \nError: {err}")
             
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
             self.combo_tipo_direccion.addItems (["casa", "dpto", "block"])

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

            #--- Tabla de socios registrados -- 
             self.tabla_socios = QTableWidget()
             self.tabla_socios.setColumnCount(5)
             self.tabla_socios.setHorizontalHeaderLabels(["RUT", "Nombre completo", "Teléfono", "Comuna", "Tipo Vivienda"])

            #agregar la tabla al layout de socios
             layout_socios.addWidget(self.tabla_socios)

             #----Pantalla 2: Clases dirigidas--
             self.vista_clases=QWidget()
             layout_clases = QVBoxLayout()
             self.vista_clases.setLayout(layout_clases)

             #subtitulo de la sección
             lbl_titulo_clases = QLabel ("🧘 Registro y Gestión de Clases Dirigidas")
             lbl_titulo_clases.setStyleSheet ("font-size: 18px; font-weight: bold; color: #2C3E50;")
             layout_clases.addWidget(lbl_titulo_clases)

             #Formulario de la clase
             form_clases = QFormLayout()

             self.combo_tipo_clase = QComboBox()
             self.combo_tipo_clase.addItems (["Yoga", "Spinning", "Crossfit"])

             self.input_nombre_clase = QLineEdit()
             self.input_nombre_clase.setPlaceholderText("Ej: Yoga Matinal")

             self.input_cupo_maximo = QLineEdit()
             self.input_cupo_maximo.setPlaceholderText("Ej: 15")

             self.input_duracion = QLineEdit()
             self.input_duracion.setPlaceholderText("Duración en minutos (Ej: 60)")

             self.input_especifico_clase = QLineEdit()
             self.input_especifico_clase.setPlaceholderText("Nivel (Inicial/Intermedio/Avanzado)")

             form_clases.addRow("Disciplina:", self.combo_tipo_clase)
             form_clases.addRow("Nombre Clase:", self.input_nombre_clase)
             form_clases.addRow("Cupo Máximo: ", self.input_cupo_maximo)
             form_clases.addRow("Duración (min): ", self.input_duracion)
             form_clases.addRow("Detalle Específico", self.input_especifico_clase)

             layout_clases.addLayout(form_clases)

             #Botón para crear claseeeee
             self.btn_guardar_clase = QPushButton("💾 Crear Clase Dirigida")
             self.btn_guardar_clase.setStyleSheet("background-color: #8E44AD; color: white; padding: 8px; font-weight: bold;")

             layout_clases.addWidget(self.btn_guardar_clase)
             self.btn_guardar_clase.clicked.connect(self.guardar_clase)

            #Tabla de clases dirigidas
             self.tabla_clases = QTableWidget()
             self.tabla_clases.setColumnCount(5)
             self.tabla_clases.setHorizontalHeaderLabels(["Disciplina", "Nombre Clase", "Cupo Máximo", "Duración (min)", "Detalle Específico"])

             layout_clases.addWidget(self.tabla_clases)


             #-----Pantalla 3 
             self.vista_ventas = QWidget()
             layout_ventas = QVBoxLayout()
             self.vista_ventas.setLayout(layout_ventas)

             self.btn_obtener_dolar = QPushButton("🌐 Cargar Dólar Oficial en Vivo")
             self.btn_obtener_dolar.setStyleSheet("backgroud-color: #16A095; color: white; padding: 5px")
             self.btn_obtener_dolar.clicked.connect(self.cargar_dolar_api)

            
             #Subtitulo de la sección
             lbl_titulo_ventas = QLabel ("🛒 Punto de Venta y Gestión de Inventario")
             lbl_titulo_ventas.setStyleSheet("font-size: 18px; font-weight: bold; color: #2C3E50;")
             layout_ventas.addWidget(lbl_titulo_ventas)

             #formulario de ventas
             form_ventas = QFormLayout()
             
             self.combo_producto = QComboBox()
             self.combo_producto.addItems(["Proteína Whey 1kg", "Creatina Monohidratada 300g", "BCAA 500g", "Pre-Workout 300g"])

    
             self.input_cantidad = QLineEdit()
             self.input_cantidad.setPlaceholderText("Ej: 2")

             self.input_valor_dolar = QLineEdit()
             self.input_valor_dolar.setPlaceholderText("Ej: 950 (Valor CLP del dólar)")   

             form_ventas.addRow("Producto Suplemento: ", self.combo_producto)
             form_ventas.addRow("Cantidad a vender: ", self.input_cantidad)
             form_ventas.addRow("Valor dólar (CLP): ", self.input_valor_dolar)
             form_ventas.addRow("Consultar API: ", self.btn_obtener_dolar)

            
             layout_ventas.addLayout(form_ventas)

             #Botón de procesar venta
             self.btn_guardar_venta = QPushButton("💳 Procesar Venta")
             self.btn_guardar_venta.setStyleSheet("background-color: #2980B9; color:white; padding: 8px; font-weight: bold;")

             layout_ventas.addWidget(self.btn_guardar_venta)
             self.btn_guardar_venta.clicked.connect(self.guardar_venta)

             #Tabla historialis de ventis
             self.tabla_ventas = QTableWidget()
             self.tabla_ventas.setColumnCount(4)
             self.tabla_ventas.setHorizontalHeaderLabels(["Producto", "Cantidad", "Valor Dólar", "Total Estimado (CLP)"])

             layout_ventas.addWidget(self.tabla_ventas)
             
             #Agregar las 3 vistas a la pila de pantallas (índices.0 1 y 2)
             self.pantallas.addWidget(self.vista_socios) #index 0
             self.pantallas.addWidget(self.vista_clases) #index 1
             self.pantallas.addWidget(self.vista_ventas) #index 2

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