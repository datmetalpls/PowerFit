## [1.0.0] - 2026-10-05

### 🚀 Añadido (Fase 5 - Evaluación Sumativa 2)
- **Persistencia (SQLite & DAO)**:
  - Implementación completa de operaciones CRUD transaccionales a través del patrón DAO en `src/dao/`.
  - Base de datos relacional `powerfit.db` gestionada automáticamente y prevención contra inyección SQL usando consultas preparadas (`?`).
  - Almacenamiento seguro de transacciones como Venta y Detalles de Venta.
- **Seguridad y Validación (Excepciones Propias)**:
  - Creación del archivo `src/models/excepciones.py` conteniendo las reglas de negocio como excepciones controladas (`SinCupoException`, `MembresiaVencidaException`).
  - Validación fuerte en setters con `ValueError` (ej. al instanciar un RUT inválido o un stock negativo).
  - Captura y manejo visual de todas las excepciones con bloques `try/except` en `src/gui/app_window.py` mostrando avisos amigables (`QMessageBox`) sin detener el programa.
- **Uso de IA documentado**:
  - Actualización del `README.md` documentando el caso práctico de adaptación del algoritmo de validación Módulo 11 sugerido por IA, integrando lanzamiento de excepciones (`ValueError`) en lugar de detención abrupta (`sys.exit()`).

# 📜 Changelog - PowerFit

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

## [0.9.2] - 2026-10-04

### 🚀 Integración Total de Interfaz Gráfica PySide6 & Persistencia SQLite (`src/gui/app_window.py`)
- **Módulo de Clases e Inscripciones Conectado a SQLite**:
  - `guardar_clase()`: Persistencia permanente de clases dirigidas con `ClaseDAO`.
  - `hacer_clic_puesto()`: Registro automático de inscripciones en `InscripcionDAO` e integración con la validación formal de asistencias por Instructores.
- **Módulo de Punto de Venta & Inventario Conectado a SQLite**:
  - `reponer_stock_admin()`: Reposición física de suplementos por Administrador persistida en la base de datos mediante `SuplementoDAO`.
  - `guardar_venta()`: Validación transaccional de stock en SQLite y actualización automática tras procesar ventas.
- **Módulo de Personal Conectado a SQLite**:
  - `guardar_trabajador_admin()`: Registro y alta de trabajadores (Recepcionistas, Instructores, Administradores) persistidos permanentemente con `TrabajadorDAO`.
- **Estabilidad & Calidad de Código**:
  - Eliminación de código duplicado en el renderizado de la tabla de socios (`actualizar_tabla_socios()`).
  - Verificación sin errores de compilación ni de tiempo de ejecución.


### 🗄️ Implementación Completa de Capa DAO SQLite (`src/dao/`)
- **Esquema Relacional DDL (`ConexionDB.crear_tablas`)**:
  - Sentencias `CREATE TABLE IF NOT EXISTS` para `socios`, `trabajadores`, `clases`, `inscripciones` y `suplementos`.
  - Activación de restricciones de Foreign Keys (`PRAGMA foreign_keys = ON;`) y soporte para mapeo dinámico por columnas.
- **Jerarquía y Contrato Abstracto (`BaseDAO`)**:
  - `src/dao/base_dao.py`: Clase abstracta genérica definiendo los contratos CRUD (`obtener_todos`, `obtener_por_id`, `guardar`, `eliminar`).
- **Data Access Objects Concretos**:
  - `SocioDAO`: Persistencia completa con soporte para `obtener_por_rut()` y lógica UPSERT.
  - `TrabajadorDAO`: Instanciación polimórfica adecuada para `Administrador`, `Instructor` y `Recepcionista`.
  - `ClaseDAO`: Mapeo polimórfico a subclases de disciplina concretas (`Spinning`, `Yoga`, `Crossfit`).
  - `SuplementoDAO`: CRUD completo para inventario y catálogo de suplementos.
  - `InscripcionDAO`: Persistencia de inscripciones y registro de asistencia en clases dirigidas.
- **Suite de Pruebas Unitarias (`tests/`)**:
  - Pruebas dedicadas `tests/test_socio_dao.py` y `tests/test_trabajador_dao.py` para verificar lectura/escritura SQLite.

### 🖥️ Integración Inicial GUI (`src/gui/app_window.py`)
- **Sincronización al Iniciar (`cargar_datos_desde_bd`)**:
  - Carga automática de Socios, Clases y Usuarios del sistema desde `powerfit.db`.
  - Si la base de datos está vacía, sembrado automático de usuarios iniciales (`admin`, `recepcion`, `instructor`).
- **Persistencia en Gestión de Socios**:
  - Registro de nuevo socio, renovación de mensualidad y cancelación de plan persistidos permanentemente en SQLite a través de `SocioDAO`.


### 🗄️ Inicialización de Capa DAO e Infraestructura SQLite
- **Paquete DAO (`src/dao/`)**:
  - Creación del paquete `src/dao/` y los esqueletos de DAO para `SocioDAO`, `TrabajadorDAO`, `ClaseDAO`, `InscripcionDAO` y `SuplementoDAO`.
  - Implementación de `ConexionDB` en `src/dao/conexion.py` con cálculo de ruta dinámica `database/powerfit.db`, activación de Foreign Keys (`PRAGMA foreign_keys = ON`) y formato de filas por nombre (`sqlite3.Row`).
- **Infraestructura de Base de Datos**:
  - Creación del directorio `database/` con `.gitkeep` y actualización de `.gitignore` para el aislamiento de archivos SQLite `.db`.


### 🧹 Limpieza y Optimización de Dependencias
- **Depuración de `requirements.txt`**:
  - Eliminación de dependencias innecesarias/no utilizadas (`fastapi`, `uvicorn`, `pydantic`, `python-dotenv`, `pyyaml`, `requests`, `pytest`, `shiboken6`, etc.).
  - Consolidación de dependencias requeridas del proyecto (`PySide6>=6.7.0` para la GUI y `matplotlib>=3.8.0` para la generación de infografías).


### 🔐 Ajuste Estricto de Perfilamiento RBAC (Instructor & Recepcionista)
- **Restricción de Accesos para Instructor (`src/gui/app_window.py`)**:
  - `btn_torniquete.setVisible(False)`: Se ocultó explícitamente el simulador de Torniquete / Portería al iniciar sesión como Instructor.
  - El Instructor tiene acceso **exclusivo** a la pestaña **"🏋️ Clases Dirigidas"** (con Socios, Ventas, Personal y Torniquete bloqueados).
  - Redirección automática inicial del Instructor hacia la vista de Clases Dirigidas.
- **Invocación Formal de Asistencia por Instructor**:
  - Al inscribir o marcar un socio desde el perfil del Instructor en el mapa de sala, el sistema ejecuta formalmente el método del modelo POO `Instructor.marcarAsistencia(socio, clase)`.
- **Consolidación de Roles Recepcionista y Administrador**:
  - Recepcionista: Acceso habilitado a Gestión de Socios, Punto de Venta (Dólar API) y Torniquete de Portería.
  - Administrador: Acceso total a los 5 módulos del sistema.

## [0.8.0] - 2026-09-26

### 🎨 Modularización de la Capa de Interfaz Gráfica (`src/gui/`)
- **Desacople de Presentación & Bootstrap Limpio (`main.py`)**:
  - Traslado de la arquitectura visual de PySide6 a un paquete dedicado en `src/gui/`.
  - `src/gui/styles.py`: Extracción de las hojas de estilo QSS `QSS_MODO_OSCURO` y `QSS_MODO_CLARO` para el tema Cyber-Gym.
  - `src/gui/app_window.py`: Clase `VentanaPrincipalPowerFit` encapsulada en su propio módulo, manteniendo el 100% de la funcionalidad de formularios, mapas de sala, simulación de torniquete y perfilamiento RBAC.
  - `main.py`: Reducido a solo **20 líneas de código** actuando como un bootstrap limpio que inicia la aplicación visual.
- **Preparación de Arquitectura para la Fase 6 (Persistencia SQLite / Patrón DAO)**:
  - Estructura limpia y aislada que facilita la integración futura de la capa de persistencia relacional.


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
