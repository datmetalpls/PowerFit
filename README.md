# 🏋️ PowerFit - Sistema de Gestión de Gimnasio

Sistema desarrollado en Python bajo el paradigma de **Programación Orientada a Objetos (POO)** para la asignatura de POO. El proyecto implementa los requerimientos de negocio y diseño estructural UML especificados en la arquitectura del sistema.

---

## 📌 Estado de la Clase `Persona` (`persona.py`)

La clase `Persona` actúa como la plantilla base (clase abstracta padre) para representar a todos los individuos del sistema (Socios, Trabajadores, Instructores, Recepcionistas, etc.).

### 📋 Atributos
Todos los atributos han sido definidos con anotaciones de tipo y alineados estrictamente con el diagrama UML (`UML/ProyectGym.drawio`):

| Atributo | Tipo | Descripción |
| :--- | :--- | :--- |
| `rut` | `str` | Identificador único nacional de la persona |
| `nombres` | `str` | Nombres de la persona (plural según especificación UML) |
| `apellidoPaterno` | `str` | Primer apellido de la persona |
| `apellidoMaterno` | `str` | Segundo apellido de la persona |
| `telefono` | `str` | Número telefónico de contacto |
| `correoElectronico` | `str` | Dirección de correo electrónico de contacto |

### 🛠️ Métodos

#### Constructor `__init__`
Inicializa todos los atributos obligatorios al instanciar una objeto `Persona`:
```python
def __init__(self, rut: str, nombres: str, apellidoPaterno: str, apellidoMaterno: str, telefono: str, correoElectronico: str)
```

#### Métodos Getter y Setter (Encapsulamiento)
- **Getters (lectura)**: `getRut()`, `getNombres()`, `getApellidoPaterno()`, `getApellidoMaterno()`, `getTelefono()`, `getCorreoElectronico()`.
- **Setters (modificación)**: `setTelefono(telefono)`, `setCorreoElectronico(correoElectronico)` (los atributos de identidad se conservan protegidos e inmutables).

#### Métodos de Validación (UML)
- **`validarRut() -> bool`**: Valida la autenticidad del RUT y su dígito verificador mediante el **Algoritmo Módulo 11** (soporta puntos, guión, espacios y dígito verificador 'K').
- **`validarTelefono() -> bool`**: Valida que el formato telefónico sea válido.
- **`validarCorreoElectronico() -> bool`**: Valida el formato del correo electrónico de la persona.

---

## 📌 Estado de la Clase `Direccion` (`direccion.py`)

La clase `Direccion` representa la ubicación física y postal dentro del sistema PowerFit.

### 📋 Atributos
Todos los atributos han sido definidos con anotaciones de tipo y alineados estrictamente con el diagrama UML (`UML/ProyectGym.drawio`):

| Atributo | Tipo | Descripción |
| :--- | :--- | :--- |
| `idDireccion` | `int` | Identificador único de la dirección |
| `tipoDireccion` | `str` | Tipo de vivienda (`'casa'`, `'dpto'`, `'block'`) |
| `calle` | `str` | Nombre de la calle o avenida |
| `numero` | `str` | Número de la dirección |
| `referencia` | `str` | Información adicional o referencia de llegada |

### 🛠️ Métodos y Encapsulamiento

#### Constructor `__init__`
Inicializa y valida los datos de la dirección al instanciar:
```python
def __init__(self, idDireccion: int, tipoDireccion: str, calle: str, numero: str, referencia: str)
```
- Incluye validación para `tipoDireccion` permitiendo únicamente: `'casa'`, `'dpto'` o `'block'` (ignorando mayúsculas y espacios en blanco). En caso de ingresar un valor inválido, lanza un `ValueError`.

#### Métodos Getter y Setter (Encapsulamiento)
- **Getters (lectura)**: `getIdDireccion()`, `getTipoDireccion()`, `getCalle()`, `getNumero()`, `getReferencia()`.
- **Setters (modificación)**: `setIdDireccion()`, `setTipoDireccion()`, `setCalle()`, `setNumero()`, `setReferencia()`.
  - `setTipoDireccion(tipoDireccion)`: Aplica la misma regla de validación restringida que el constructor.

---

## 🧪 Pruebas Unitarias (`test.py`)

Se cuenta con un script de pruebas unitarias ([`test.py`](./test.py)) para validar el comportamiento del método `validarRut()` ante múltiples casos reales.

### Ejecución de Pruebas
Para ejecutar las pruebas en la consola:
```bash
python3 test.py
```

Las pruebas cubren los siguientes escenarios:
- RUTs válidos con formato completo (`12.345.678-5`).
- RUTs válidos sin puntos ni guiones (`123456785`).
- RUTs válidos finalizados en dígito verificador `'K'` o `'k'` (`14.805.293-K`).
- RUTs con dígitos verificadores o cuerpo incorrectos / caracteres no numéricos.
- Casos borde como cadenas vacías o longitudes insuficientes.

---

## 📝 Historial de Cambios Realizados

A continuación se detallan las modificaciones realizadas paso a paso sobre el proyecto:

1. **Ajuste de Atributos y Eliminación Temporal del Constructor:**
   - Se declararon los atributos base `rut`, `nombre`, `apellidoPaterno`, `apellidoMaterno`, `telefono` y `correoElectronico` con sus correspondientes anotaciones de tipo `str`.

2. **Alineación de Nombres con Diagrama UML e Inclusión del Constructor `__init__`:**
   - Se corrigió el nombre del atributo de `nombre` a **`nombres`** (en plural) para mantener 100% de coherencia con el diagrama UML (`ProyectGym.drawio`).
   - Se definió el método constructor `__init__` asignando cada uno de los 6 atributos requeridos.

3. **Inclusión de Métodos de Validación y Comentarios:**
   - Se incorporaron los métodos `validarRut()`, `validarTelefono()` y `validarCorreoElectronico()`.
   - Se agregaron comentarios explicativos y docstrings detallados en cada sección de la clase.

4. **28-09-2026 SE AGREGARON GET Y SET DE LOS ATRIBUTOS:**
   - Se encapsularon los atributos de la clase con prefijo `_`.
   - Se implementaron métodos `get` para todos los atributos: `getRut()`, `getNombres()`, `getApellidoPaterno()`, `getApellidoMaterno()`, `getTelefono()` y `getCorreoElectronico()`.
   - Se implementaron métodos `set` para aquellos atributos editables de contacto: `setTelefono()` y `setCorreoElectronico()`.

5. **IMPLEMENTACIÓN DEL ALGORITMO MÓDULO 11 EN `validarRut()` Y CREACIÓN DE `test.py`:**
   - Se implementó el algoritmo de Módulo 11 en el método `validarRut()` de la clase `Persona`.
   - Se creó e integró el script `test.py` para pruebas automatizadas del validador de RUT.

6. **Implementación y validación de la Clase `Direccion` (`direccion.py`):**
   - Declaración de atributos con tipos según el diagrama UML (`idDireccion: int`, `tipoDireccion: str`, `calle: str`, `numero: str`, `referencia: str`).
   - Implementación del constructor `__init__` con encapsulamiento de atributos con prefijo `_`.
   - Implementación de métodos getters y setters para todos los atributos.
   - Validación del atributo `tipoDireccion` restringido a `"casa"`, `"dpto"` y `"block"`, sanitizando espacios y mayúsculas (`strip().lower()`).

---

## 📁 Estructura del Repositorio

- `persona.py`: Implementación de la clase `Persona`.
- `direccion.py`: Implementación de la clase `Direccion` con validación de tipo de vivienda.
- `test.py`: Suite de pruebas unitarias automatizadas para validar el comportamiento de los métodos de `Persona`.
- `UML/ProyectGym.drawio`: Diagrama UML de clases oficial del proyecto.
- `Requirements/`: Documentación del levantamiento de requerimientos y auditoría del diseño UML.


