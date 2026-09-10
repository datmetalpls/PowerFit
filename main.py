"""PowerFit - Punto de entrada principal."""

import sys
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QVBoxLayout,
    QPushButton,
    QMessageBox,
)
from src.models import Persona, Direccion, cargar_comunas_ine
import uuid

# Clase de la ventana heredando de QWidget
class VentanaRegistro(QWidget):
    def __init__(self):
        super().__init__()
        # Configuración básica de la ventana
        self.setWindowTitle("PowerFit - Registro de Persona")
        self.resize(350, 250)

        # Layout principal (organiza elementos de forma vertical)
        layout = QVBoxLayout()

        # Componentes de la interfaz
        self.lbl_titulo = QLabel("Ingrese los datos de la persona:")
        self.input_rut = QLineEdit()
        self.input_rut.setPlaceholderText("Ej: 12345678-9")

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Nombre Completo")

        self.btn_guardar = QPushButton("Guardar Registro")
        # Conectar el botón a un método (evento click)
        self.btn_guardar.clicked.connect(self.guardar_datos)

        # Agregar los componentes al layout
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.input_rut)
        layout.addWidget(self.input_nombre)
        layout.addWidget(self.btn_guardar)

        # Asignar el layout a la ventana
        self.setLayout(layout)

    # Método de la clase
    def guardar_datos(self):
        rut = self.input_rut.text()
        nombre = self.input_nombre.text()
        
        # Imprime en la consola/terminal
        print(f"Datos Ingresados -> RUT: {rut}, Nombre: {nombre}")
        
        # Muestra una ventana emergente gráfica
        QMessageBox.information(
            self,
            "Registro Exitoso",
            f"Persona registrada correctamente:\nRUT: {rut}\nNombre: {nombre}"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 1. Crear la app
    ventana = VentanaRegistro()   # 2. Crear tu ventana POO
    ventana.show()                # 3. Mostrarla en pantalla
    sys.exit(app.exec())          # 4. Iniciar bucle de eventos






Usuario=Persona("2111111-K", "César", "Guerrero", "Acevedo", "+56333434342", "correo@notiene.cl")
comu_ine=cargar_comunas_ine()

print(Usuario.getRut())
print(Usuario.getNombres())

id_autogenerado=str(uuid.uuid4())
domicilio=Direccion(id_autogenerado, "Casa", "Ramon Venegas", 3116, "El parque")

print("ID: ", domicilio.getIdDireccion(), "\n", "Calle:", domicilio.getCalle(), "\n", "Número: ", domicilio.getNumero(), "\n", "Calle Referencia: ", domicilio.getReferencia(), "\n", "Comuna: ", comu_ine.get(13101).nombre)