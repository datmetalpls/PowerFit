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
)
from src.models import Persona, Direccion, cargar_comunas_ine
from PySide6.QtCore import Qt
import uuid

class VentanaPrincipalPowerFit(QMainWindow):
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

             #crear 3 vistas temporales simples (widgets)
             self.vista_socios = QLabel("🏋️ Pantalla de Gestión de Socios")
             self.vista_socios.setAlignment(Qt.AlignCenter)

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