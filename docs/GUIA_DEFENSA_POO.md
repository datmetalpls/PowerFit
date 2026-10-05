# 🛡️ Guía de Defensa - Evaluación Sumativa 2 (PowerFit)

Este documento resume exactamente en qué partes del código de **PowerFit** se cumplen los criterios exigidos por la rúbrica de evaluación. Ideal para preparar la demostración y la defensa oral.

---

## 1. Los 4 Pilares de la Programación Orientada a Objetos (POO)

El proyecto hace un uso intensivo de los 4 paradigmas fundamentales de la POO en la carpeta `src/models/`:

### A. Abstracción
Se extraen las características esenciales de entidades generales y se delega la implementación a las clases hijas.
- **Dónde se aplica:** Las clases `Persona`, `Clase` y `Trabajador` heredan de `ABC` (Abstract Base Class). 
- **Ejemplo:** En `clase.py`, se define el método `@abstractmethod def calcularCuposDisponibles(self)`, obligando a cada disciplina a definir cómo se calcula su cupo según su propio recurso físico.

### B. Herencia
Permite crear nuevas clases basadas en clases existentes, promoviendo la reutilización de código mediante `super().__init__()`.
- **Dónde se aplica:** 
  - `Socio`, `Trabajador` heredan de `Persona` (reutilizando RUT, nombre, contacto).
  - `Instructor`, `Recepcionista` y `Administrador` heredan de `Trabajador`.
  - `Yoga`, `Spinning` y `Crossfit` heredan de `ClaseDirigida` (que a su vez hereda de `Clase`).

### C. Polimorfismo
Permite que diferentes objetos respondan al mismo método de formas distintas.
- **Dónde se aplica:** En el método `calcularCuposDisponibles()`. 
  - Al llamar a este método en un objeto `Yoga`, calcula en base a `_colchonetas`. 
  - En un objeto `Spinning`, calcula en base a `_bicicletas`.
  - En un objeto `Crossfit`, calcula en base a `_estacionesTrabajo`.

### D. Encapsulamiento
Protección y ocultamiento del estado interno de los objetos.
- **Dónde se aplica:** Todos los atributos del modelo son **privados** (ej. `self._rut`, `self._stock`, `self._estadoActivo`). Para acceder a ellos desde fuera, se utilizan propiedades (`@property` para *Getters* y `@atributo.setter` para *Setters*).

---

## 2. Validación en Setters (Seguridad de Entradas)

La pauta exige que los datos se validen en el setter y rechacen datos inválidos con un mensaje sin detener el programa.
- **Validación de RUT:** En `src/models/persona.py`, el `@rut.setter` intercepta el cambio de RUT. Utiliza internamente el algoritmo matemático de Módulo 11 (`validarRut()`). Si el RUT es matemáticamente falso, arroja un `ValueError("El RUT no es válido")`.
- **Validación de Stock:** En `src/models/suplemento.py`, el `@stock.setter` impide inyectar inventario negativo levantando un `ValueError`.
- **En la Interfaz (GUI):** Estos errores (`ValueError`) son capturados por bloques `try/except` en `src/gui/app_window.py` (ej. al guardar un Socio). Se detiene el proceso de guardado y se muestra un `QMessageBox.critical` en pantalla **sin "crashear"** el programa.

---

## 3. Excepciones Propias y Reglas de Negocio

La pauta exige que las dos reglas de negocio que impiden una operación lancen su **propia excepción** (no excepciones genéricas de Python) y se capturen.
- Se creó el archivo `src/models/excepciones.py` definiendo: `MembresiaVencidaException` y `SinCupoException`.
- **Regla 1 (Falta de Cupo Físico):** Al intentar inscribir a alguien (`reservarCupo()` o `inscribir_socio()` en `clase.py`), si el cálculo polimórfico indica que no hay espacio, se lanza un `SinCupoException`.
- **Regla 2 (Membresía Vencida):** El método `permitirIngreso()` en `socio.py` revisa las fechas y el estado activo. Si el plan está vencido o cancelado, lanza un `MembresiaVencidaException`.
- **Control de Estabilidad:** En la GUI (`app_window.py`), estas excepciones son atrapadas mediante `try/except MembresiaVencidaException`, informando a la Recepcionista del rechazo mediante una ventana emergente.

---

## 4. Consumo de Servicios Externos (API)

El sistema necesita un precio que dependa de un indicador externo y que no detenga el programa si se cae el internet.
- **Implementación:** En `src/models/suplemento.py`, la clase `IndicadorDolar` utiliza la librería oficial de Python `urllib.request` y `json` para hacer una petición GET a `https://mindicador.cl/api/dolar`.
- **Manejo de Caídas:** Se le configuró un `timeout=3`. El bloque entero está dentro de un `try/except`. Si el servidor del gobierno se cae o no hay internet, la excepción asigna un valor seguro por defecto (Fallback de `$950`), garantizando que las **Ventas no se detengan**. 

---

## 5. Persistencia (Base de Datos Relacional local)

La información no muere al cerrar la aplicación.
- **SQLite y DAO:** Se utiliza `sqlite3`. El código de base de datos está segregado en el patrón DAO (`src/dao/`), separando completamente las consultas SQL de los modelos POO puros. 
- **Transacción Maestro-Detalle:** El CRUD más complejo se visualiza en `venta_dao.py`, donde guardar una `Venta` inserta primero el registro principal (Maestro) y luego itera para insertar cada `DetalleVenta` asociado.
- **Seguridad Antihackeo:** En todo el CRUD se usaron sentencias parametrizadas (ej. `VALUES (?, ?, ?)`), lo cual mitiga al 100% las vulnerabilidades de **Inyección SQL**.

---

## 6. Ajuste y Documentación de IA (README)

Se dio cumplimiento explícito en el `README.md` a documentar una decisión técnica tomada junto a una IA:
- Se explicó cómo la IA sugirió originalmente validar el RUT usando `sys.exit()` (lo que cierra de golpe la interfaz gráfica). La decisión técnica humana fue adoptar la matemática sugerida, pero descartar el apagado forzado para, en su lugar, emitir un `ValueError` limpio atrapable por PySide6.
