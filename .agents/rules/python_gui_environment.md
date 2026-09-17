# 🐍 Reglas de Entorno Python 3.12 & PySide6 (PowerFit)

## 1. Versión de Python Requerida
- Usar **Python 3.12** como la versión oficial y estable para el desarrollo de la GUI con PySide6.
- **NO utilizar versiones bleeding-edge / inestables (como Python 3.14)** debido a la falta de binarios C++ compilados para el plugin de plataforma `cocoa` de Qt en macOS.

## 2. Gestión del Entorno Virtual (.venv)
- Ante cambios de ruta o renombramiento del directorio del proyecto, regenerar siempre el `.venv`:
  ```bash
  python3.12 -m venv --clear .venv
  ./.venv/bin/pip install -r requirements.txt
  ```

## 3. Comandos Estándar de Ejecución
- **Interfaz Gráfica GUI (PySide6)**:
  ```bash
  ./.venv/bin/python main.py
  ```
- **API Backend (FastAPI / Uvicorn)**:
  ```bash
  ./.venv/bin/uvicorn api.api:app --reload
  ```
- **Pruebas Unitarias**:
  ```bash
  ./.venv/bin/python tests/test_persona.py
  ```
