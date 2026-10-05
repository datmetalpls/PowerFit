"""PowerFit - Punto de entrada principal a la aplicación PySide6.

Este archivo actúa como el bootstrap del sistema, instanciando QApplication
y ejecutando la ventana principal cargada desde el paquete src.gui.
"""
import sys
from PySide6.QtWidgets import QApplication
from src.gui.app_window import VentanaPrincipalPowerFit


def main():
    """Inicializa y ejecuta el loop principal de la aplicación GUI."""
    app = QApplication(sys.argv)
    ventana = VentanaPrincipalPowerFit()
    ventana.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()