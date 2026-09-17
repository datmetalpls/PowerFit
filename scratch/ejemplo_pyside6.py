import sys
from pathlib import Path

# Aseguramos que Python encuentre el paquete 'src' desde la carpeta scratch
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, 
    QLabel, QLineEdit, QPushButton
)
from PySide6.QtCore import Qt

# Importamos la clase Persona de nuestro paquete src.models
from src.models import Persona


class VentanaValidadorRut(QWidget):
    """Ventana interactiva creada con POO heredando de QWidget."""

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # 1. Configuración de la ventana
        self.setWindowTitle("PowerFit - Validador de RUT (PySide6)")
        self.setFixedSize(400, 220)

        # 2. Creación de componentes (Widgets)
        self.lbl_titulo = QLabel("Ingrese RUT para validar:")
        self.lbl_titulo.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.txt_rut = QLineEdit()
        self.txt_rut.setPlaceholderText("Ej: 12.345.678-K")

        self.btn_validar = QPushButton("Validar RUT con Módulo 11")
        
        self.lbl_resultado = QLabel("")
        self.lbl_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # 3. Conexión del Evento (SIGNAL -> SLOT)
        self.btn_validar.clicked.connect(self.validar_rut)

        # 4. Organización del Layout (Diseño Vertical)
        layout = QVBoxLayout()
        layout.addWidget(self.lbl_titulo)
        layout.addWidget(self.txt_rut)
        layout.addWidget(self.btn_validar)
        layout.addWidget(self.lbl_resultado)

        self.setLayout(layout)

    # --- SLOT (Método que responde al clic del botón) ---
    def validar_rut(self):
        rut_ingresado = self.txt_rut.text()

        # Instanciamos la clase Persona
        persona_temp = Persona(
            rut=rut_ingresado,
            nombres="Prueba",
            apellidoPaterno="Test",
            apellidoMaterno="Test",
            telefono="912345678",
            correoElectronico="test@powerfit.cl"
        )

        # Invocamos el método de validación
        es_valido = persona_temp.validarRut()

        # Actualizamos la interfaz
        if es_valido:
            self.lbl_resultado.setText("✅ RUT Válido (Algoritmo Módulo 11)")
            self.lbl_resultado.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.lbl_resultado.setText("❌ RUT Inválido o Formato Incorrecto")
            self.lbl_resultado.setStyleSheet("color: red; font-weight: bold;")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaValidadorRut()
    ventana.show()
    sys.exit(app.exec())
