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
             lbl_bienvenida.setStyleSheet("font-size: 24px; font-weight: bold; color: $2C3E50")
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