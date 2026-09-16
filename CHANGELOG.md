# 📜 Changelog - PowerFit

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### ⚙️ Entorno & Compatibilidad de Python
- **Estandarización de Versión de Python (Python <= 3.12)**:
  - Se estableció **Python 3.12** como la versión máxima recomendada y estable para el proyecto.
  - Se restringió el uso de versiones experimentales o *bleeding-edge* (como **Python 3.14**) debido a la falta de soporte de binarios C++ para el plugin de plataforma `cocoa` de Qt / PySide6 en macOS.
  - Reconfiguración del entorno virtual `.venv` alineado con Python 3.12.

### 🎨 Documentación Visual & Perfilamiento (Hito 6)
- **Infografía de Perfilamiento RBAC (`docs/powerfit_rbac_profiles.jpg`)**:
  - Matriz visual de permisos y roles (Administrador, Recepcionista, Instructor).
  - Integración del diagrama visual en `README.md` y `docs/requirements/Auditoria-y-Correcciones-UML-PowerFit.md`.

### 💡 Próximos pasos (Hito 6 GUI - Perfilamiento & Autenticación)
- Pantalla de inicio de sesión (Login) por usuario y contraseña.
- Control de acceso por rol (Administrador, Recepcionista, Instructor).
- Integración de credenciales con la API del backend (`api/admin.py`).
- Refactorización modular de `main.py` hacia la carpeta `gui/`.

## [0.3.0] - 2026-09-15

### 🎨 Interfaz Gráfica (PySide6)
- **Marco Principal (`QMainWindow`)**:
  - Ventana de 800x600 px con título personalizado y estilos CSS.
  - Menú navegable con botones animados (`QPushButton:hover`).
  - Navegación multitarea fluida en tiempo real usando `QStackedWidget`.
  - Barra de estado inferior (`statusBar()`) para mensajes del sistema.
- **Módulo de Gestión de Socios**:
  - Formulario estructurado con `QFormLayout`.
  - Campos completos de datos personales y atributos UML de `Direccion` (`casa`, `dpto`, `block`, calle, número, referencia).
  - Desplegable `QComboBox` cargando dinámicamente las 346 comunas de Chile (`cargar_comunas_ine()`).
  - **Tabla `QTableWidget` de Socios**: Inserción en tiempo real de filas con RUT, Nombre, Teléfono, Comuna y Tipo de vivienda.
  - Validación de campos y alertas interactivas `QMessageBox`.
- **Módulo de Clases Dirigidas**:
  - Formulario para registro de disciplinas (`Yoga`, `Spinning`, `Crossfit`).
  - Campos de cupo máximo, duración y detalles específicos por disciplina.
  - **Tabla `QTableWidget` de Clases**: Listado interactivo en vivo con Disciplina, Nombre, Cupos, Duración y Detalle Específico.
- **Módulo de Ventas & Integración API Dólar**:
  - Punto de venta de suplementos deportivos.
  - Integración en tiempo real con la **API de `mindicador.cl`** mediante botón **`🌐 Cargar Dólar Oficial en Vivo`** autocompletando la tasa oficial del día en CLP.
  - **Tabla `QTableWidget` de Historial de Ventas**: Listado dinámico con Producto, Cantidad, Valor Dólar y Total Estimado en CLP.
- **Documentación & Recursos Visuales**:
  - Infografía visual del Roadmap GUI v2.0 (`docs/roadmap_gui_powerfit.jpg`).



## [0.2.0] - 2026-09-10

### 🔄 Refactorización & Arquitectura
- Reorganización de la raíz en estructura modular por capas (`src/models/`, `tests/`, `docs/`, `scratch/`).
- Migración de `persona.py`, `comuna.py` y `direccion.py` a `src/models/`.
- Reubicación de la suite de pruebas unitarias a `tests/test_persona.py` con resolución automática de `sys.path`.
- Centralización de requerimientos, diagramas UML e infografía del Roadmap en `docs/`.

### 📚 Documentación
- Creado documento y gráfico de comparativa de frameworks GUI en Python (`docs/requirements/Comparativa-GUI-Tkinter-PySide-PyQt.md` e imagen infográfica).

---


## [0.1.0] - 2026-09-09

### 🚀 Añadido (Fase 1 - Fundamentos & Modelos Base)
- **Clase `Persona` (`persona.py`)**:
  - Definición de clase base abstracta con atributos (`rut`, `nombres`, `apellidoPaterno`, `apellidoMaterno`, `telefono`, `correoElectronico`).
  - Encapsulamiento de atributos con convención de privacidad `_`.
  - Getters para todos los atributos y setters restrictivos únicamente para atributos de contacto (`setTelefono`, `setCorreoElectronico`).
  - Método `validarRut()` completamente funcional con **Algoritmo Módulo 11** (soporta puntos, guiones, espacios y dígito verificador 'K'/'k').
  - Declaración de firmas para `validarTelefono()` y `validarCorreoElectronico()`.
- **Clase `Direccion` (`direccion.py`)**:
  - Implementación con atributos (`idDireccion`, `tipoDireccion`, `calle`, `numero`, `referencia`).
  - Validación en constructor y `setTipoDireccion` restringida a `'casa'`, `'dpto'` y `'block'`.
  - Encapsulamiento completo con métodos getters y setters para todos los atributos.
- **Suite de Pruebas Unitarias (`test.py`)**:
  - Creada suite de pruebas unitarias para `validarRut()` en `Persona` cubriendo 10 casos de prueba (RUTs válidos formato completo, sin puntos, DV 'K'/'k', repetitivos, incorrectos, con letras, vacíos y cortos).
- **Documentación & Artefactos**:
  - Documento de auditoría UML ([`Auditoria-y-Correcciones-UML-PowerFit.md`](./Requirements/Auditoria-y-Correcciones-UML-PowerFit.md)).
  - Documento de levantamiento de requerimientos ([`Levantamiento-de-requerimientos-PowerFit.md`](./Requirements/Levantamiento-de-requerimientos-PowerFit.md)).
  - Infografía del Roadmap de desarrollo ([`roadmap_powerfit.jpg`](./roadmap_powerfit.jpg)).
  - Documentación del README ([`README.md`](./README.md)) actualizada con Roadmap por fases, estado de clases y suite de pruebas.
  - Archivo `.gitignore` para exclusión de archivos temporales (`__pycache__`, `.DS_Store`).
