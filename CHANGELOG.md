# 📜 Changelog - PowerFit

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/) y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### 💡 Próximos pasos (Fase 2 - Jerarquía de Usuarios & Roles)
- Implementación de la clase `Socio` heredando de `Persona`.
- Implementación de la clase `Trabajador` heredando de `Persona`.
- Definición de roles (`Instructor`, `Recepcionista`, `Administrador`).
- Implementación de los métodos pendientes de validación en `Persona`: `validarTelefono()` y `validarCorreoElectronico()`.

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
