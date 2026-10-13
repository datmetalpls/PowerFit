"""PowerFit - Punto de entrada principal a la aplicación PySide6.

Este archivo actúa como el bootstrap del sistema, instanciando QApplication
y ejecutando la ventana principal cargada desde el paquete src.gui.
"""
import os
import sys
from pathlib import Path

# Asegurar disponibilidad de dependencias del proyecto instaladas en .venv (como argon2-cffi)
# Se añade al final de sys.path para conservar librerías gráficas nativas ya funcionales (PySide6)
RAIZ = Path(__file__).resolve().parent
for venv_site in RAIZ.glob(".venv/lib/python*/site-packages"):
    if venv_site.exists() and str(venv_site) not in sys.path:
        sys.path.append(str(venv_site))

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