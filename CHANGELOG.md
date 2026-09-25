# 📜 Changelog - PowerFit

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.7.0] - 2026-09-25

### 🏛️ Reorganización Modular de Clases & Alineación UML Definitivo (`posiblediagrama.drawio.xml`)
- **Limpieza y Desacoplamiento de Modelos POO (`src/models/`)**:
  - Desacoplamiento de clases masivas en archivos independientes de responsabilidad única (1 archivo = 1 clase):
    - `persona.py`: Contiene únicamente la clase abstracta `Persona` con validación de RUT Módulo 11, teléfono y correo.
    - `socio.py`: Clase `Socio` con atributos `- fechaVencimientoMembresia`, `- estadoActivo` y métodos `permitirIngreso()`, `renovarMembresia()` y `cancelarPlan()`.
    - `trabajador.py`: Clase abstracta base `Trabajador` (`idTrabajador`, `passHash`, `autenticar()`, `tienePermiso()`).
    - `administrador.py`: Subclase `Administrador` con `- nivelAcceso` y métodos `crearTrabajador()`, `crearClase()`, `modificarClase()`, `reponerStock()`.
    - `instructor.py`: Subclase `Instructor` con `dictarClase()` y `marcarAsistencia()`.
    - `recepcionista.py`: Subclase `Recepcionista` con `registrarSocio()`, `cobrarMensualidad()`, `crearInscripcion()` y `registrarVenta()`.
    - `clase.py`: Clase abstracta base `Clase`, subclase abstracta `ClaseDirigida` y especializaciones `Yoga`, `Spinning`, `Crossfit`.
    - `direccion.py`: Integración de objeto `Comuna` dentro de `Direccion` con método helper `obtenerDireccionCompleta()`.

### 🚪 Simulador de Torniquete de Portería & Popups Alerta
- **Simulador Interactivo de Molinete en GUI (`main.py`)**:
  - Nueva pestaña **"🚪 Torniquete Portería"** que simula el lector físico de tarjetas/RUT a la entrada del gimnasio.
  - Invocación en tiempo real del método de regla de negocio `Socio.permitirIngreso()`.
  - **Popup Alerta Emergente (`QMessageBox.critical`)**: Alerta flotante roja inmediata al detectar a un socio con estado impago, membresía vencida o plan cancelado, indicándole dirigirse a Recepción.
- **Gestión de Personal para Administrador (RBAC)**:
  - Nueva pestaña **"👔 Personal (Admin)"** visible únicamente para rol Administrador para dar de alta trabajadores en tiempo real (`admin.crearTrabajador()`).
- **Acciones de Recepción en GUI**:
  - Botones dedicados en gestión de socios para **"💵 Cobrar Mensualidad / Renovar (+30d)"** y **"🚫 Cancelar / Desactivar Plan"**.

### 🎨 Reestilización GUI & Sistema de Temas Adaptable (macOS & Windows)
- **Tema Visual Dark Cyber-Gym (Modern UI)**:
  - Rediseño completo de la interfaz en PySide6 usando hojas de estilos QSS personalizadas.
  - Paleta de colores en tono Dark Slate (`#0F172A`), contenedores `#1E293B`, bordes `#334155` y acentos Naranja Neón (`#F97316`) con detalles Cian (`#38BDF8`).
  - Reestilización de controles `QLineEdit`, `QComboBox`, `QTableWidget`, `QGroupBox`, `QHeaderView` y `QStatusBar`.
- **Sistema Dual-Theme Adaptable (`☀️ Modo Claro` / `🌙 Modo Oscuro`)**:
  - Implementación de variables dinámicas `QSS_MODO_OSCURO` y `QSS_MODO_CLARO` con soporte multiplataforma para macOS (`-apple-system`) y Windows (`Segoe UI`).
  - Incorporación de botón conmutador en la barra superior de navegación (`btn_toggle_tema`) que conmuta en tiempo real la paleta de colores sin perder el estado de los formularios ni del usuario en sesión.
- **Optimización de Navegación & RBAC**:
  - Resaltado dinámico de la pestaña activa en la barra superior de acuerdo al tema cargado.

## [0.5.0] - 2026-09-19

### 🏛️ Refactorización Arquitectónica POO (Alineación UML Oficial del Profesor)
- **Alineación 100% con Diagrama UML Oficial (`Powerfit_Oficial_Profesor.drawio`)**:
  - **Requisito 1 (Polimorfismo en Clases Dirigidas)**:
    - Sobreescritura explícita de `calcularCuposDisponibles() -> int` en `Yoga`, `Spinning` y `Crossfit`.
    - Atributos fijos de recursos físicos delimitadores: `colchonetas: int`, `bicicletas: int` y `estacionesTrabajo: int`.
  - **Requisito 2 (Permisos por Rol de Trabajador)**:
    - `Trabajador`: Atributo `- idTrabajador: String` y método `tienePermiso(accion: String): boolean`.
    - `Instructor`: Métodos `dictarClase(clase: ClaseDirigida)` y `marcarAsistencia(socio: Socio, clase: ClaseDirigida)`.
    - `Recepcionista`: Métodos `registrarSocio(socio: Socio)`, `cobrarMensualidad(socio: Socio, monto: float)` y `crearInscripcion(socio: Socio, mes: int, anio: int)`.
  - **Requisito 3 (Validación de Datos Identidad)**:
    - Algoritmo Módulo 11 en `Persona.validarRut() -> bool`.
  - **Requisito 4 (Transacción Compuesta de Inscripciones)**:
    - Creados nuevos modelos en `src/models/inscripcion.py`:
      - `InscripcionMensual` (mes, anio, socio, detalles).
      - `DetalleInscripcion` (diaSemana, clase, confirmarReserva()).
  - **Requisito 5 (Reglas de Bloqueo)**:
    - Bloqueo por cupo lleno: `ClaseDirigida.hayCupo() -> bool`.
    - Bloqueo por membresía vencida: `Socio.permitirIngreso() -> bool` evaluando `fechaVencimientoMembresia: Date`.
  - **Requisito 6 (Indicador Externo & Suplemento)**:
    - Creados nuevos modelos en `src/models/suplemento.py`:
      - `Suplemento`: Atributos USD y stock, con cálculo de precio `calcularPrecioCLP(valorDolar: float) -> float`.
      - `IndicadorDolar`: Método `obtenerValorDolar() -> float` consultando API `mindicador.cl`.

### 🎨 Mapa Visual de Salas en GUI PySide6 (`main.py`)
- **Grid Interactivo de Puestos**:
  - Representación visual en tiempo real de los puestos/bicicletas/mats según disciplina (🚲, 🧘, 🏋️).
  - Puestos Verdes 🟢 (Disponibles) y Rojos 🔴 (Ocupados con tooltip del socio).
  - Cálculo de porcentaje de ocupación en vivo (`X / Y Cupos - Z%`).

---

## [0.4.0] - 2026-09-17

### 🔐 Autenticación & Control de Acceso por Roles (RBAC - Hito 6)
- **Pantalla de Inicio de Sesión (`vista_login`)**:
  - Diseño de tarjeta flotante en `main.py` con campos de Usuario y Contraseña.
  - Autenticación dinámica de credenciales mediante el método `.autenticar()`.
  - Tarjeta de información con cuentas de prueba demo (`admin`, `recepcion`, `instructor`).
- **Navegación Dinámica según Rol (RBAC)**:
  - **Administrador** (`admin / admin123`): Acceso completo a Socios, Clases Dirigidas y Punto de Venta.
  - **Recepcionista** (`recepcion / rec123`): Acceso restrito a Socios y Punto de Venta.
  - **Instructor** (`instructor / ins123`): Acceso restrito a Clases Dirigidas.
  - Indicador dinámico del usuario activo y botón **"🔴 Cerrar Sesión"**.

### 🏋️ Jerarquía de Usuarios & Modelos POO (Fase 2)
- Integración de los modelos `Trabajador`, `Instructor`, `Recepcionista` y `Socio` en `src/models/`.
- Herencia completa de la clase base `Persona` reutilizando datos personales y encapsulamiento.
- Exportación centralizada desde `src/models/__init__.py`.
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
