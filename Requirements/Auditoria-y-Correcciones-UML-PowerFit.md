# Auditoría del Diagrama UML y Plan de Correcciones — Sistema PowerFit

Este documento contiene la auditoría técnica detallada y el **Plan de Correcciones y Mejoras** para el Diagrama UML de Clases del sistema **PowerFit**, contrastado directamente con el archivo `Levantamiento-de-requerimientos-PowerFit.md`.

---

## 1. 📊 Resumen Ejecutivo de la Evaluación

El Diagrama UML evaluado demuestra un sólido dominio de los conceptos clave de la Programación Orientada a Objetos (POO), tales como herencia, encapsulamiento, composición y modularidad.

Sin embargo, en el contexto de **ingeniería de software y levantamiento de requerimientos**, se observan dos fenómenos principales:
1. **Sobre-diseño (Over-engineering):** Incorporación de entidades no solicitadas que el cliente descartó explícitamente en el intercambio de correos (ej. direcciones complejas, comunas, contactos de emergencia).
2. **Brechas de Dominio:** Omisiones en la responsabilidad de creación/edición de clases y pequeñas ambigüedades en la multiplicidad de reservas.

---

## 2. 🔍 Matriz Comparativa: Requerimientos vs. Diagrama UML

| Requerimiento / Regla de Negocio (RN) | Estado en UML | Diagnóstico / Observación |
| :--- | :---: | :--- |
| **RN-01 / RN-02:** Validación e identificación por RUT | 🟢 Cumple | La clase `Persona` contiene `rut: String` y `validarRut(): Boolean`. |
| **RN-03 / RN-04:** Control de cupos máximos y disponibles | 🟢 Cumple | `Clase` define `cupoMaximo`, `calcularCuposDisponibles()` y `hayCupo()`. |
| **RN-05:** Agrupación de reservas en inscripción mensual | 🟡 Parcial | Existe `InscripcionMensual` y `DetalleInscripcion`, pero la multiplicidad con `Clase` es difusa. |
| **RN-06:** Bloqueo de ingreso por membresía vencida | 🟢 Cumple | `Socio` posee método `tieneMembresiaVigente()` y `MembresiaMensual` incluye `esVigente()`. |
| **RN-07 / RN-08:** Separación de roles Instructor vs. Recepcionista | 🟢 Cumple | Herencia desde `Trabajador` con métodos adecuados según cada rol. |
| **RN-09:** Descuento de stock en ventas presenciales | 🟢 Cumple | Composición `Venta` ➔ `DetalleVenta` ➔ `Suplemento` con `descontarStock()`. |
| **RN-10:** Cálculo de precio de suplementos según dólar del día | 🟢 Cumple | Implementa la clase `IndicadorDolar` y el método `calcularPrecioCLP()`. |
| **Alcance Limitado (Sin Direcciones ni Datos de Salud)** | 🔴 Incumple | **Sobre-diseño:** Se agregaron las clases `Direccion`, `Comuna` y `ContactoEmergencia` (Cliente Resp. #7 y #8). |
| **Gestión/Creación de Clases (Pendiente #173)** | 🔴 Incumple | Ni `Recepcionista` ni `Instructor` pueden crear clases. El diagrama no define quién las administra. |

---

## 3. 🛠️ Plan de Correcciones Paso a Paso

Para alinear el diagrama UML al 100% con los requerimientos entregados por la asignatura, se deben realizar las siguientes correcciones en el diseño de clases:

### ❌ Corrección 1: Eliminar Clases de Sobre-diseño (`Direccion`, `Comuna`, `ContactoEmergencia`)
* **Justificación:** En las respuestas #7 y #8 del cliente se especifica:
  > *"Para la ficha del socio necesitamos su nombre y su RUT. No tenemos un formato definido más allá... No tenemos ninguna normativa especial ni manejamos datos de salud."*
* **Acción a realizar:** 
  1. Eliminar las clases `Direccion` y `Comuna`.
  2. Eliminar la clase `ContactoEmergencia`.
  3. Si se desea mantener datos de contacto simples en `Persona`, conservar solo `telefono: String` y `correoElectronico: String`.

---

### 🔄 Corrección 2: Aclarar y Ajustar la Multiplicidad de Reservas
* **Justificación:** Una inscripción mensual (`InscripcionMensual`) contiene varios detalles de inscripción (`DetalleInscripcion`), y cada detalle corresponde a **una sola clase reservada**.
* **Acción a realizar:**
  1. Modificar la relación entre `DetalleInscripcion` y `Clase`.
  2. Establecer la multiplicidad en: `DetalleInscripcion` **`*` ────── `1`** `Clase`.
  3. Asegurar que `DetalleInscripcion` contenga el atributo `diaSemana: String` o `fechaReserva: Date` para especificar qué día se asiste a dicha clase.

---

### 👤 Corrección 3: Resolver la Gestión y Creación de Clases
* **Justificación:** En la regla **RN-07** se establece que la recepcionista **no puede** crear ni modificar clases. Sin embargo, el sistema requiere que las clases existan.
* **Acción a realizar (Elegir Opción A o B):**
  * **Opción A (Recomendada):** Crear una clase `Administrador` que herede de `Trabajador` con los métodos `crearClase(clase: Clase)` y `modificarClase(clase: Clase)`.
  * **Opción B:** Asignar los métodos `crearClase()` y `modificarClase()` a la clase `Trabajador` o a un rol superior de gestión.

---

### 🧹 Corrección 4: Depuración de la Jerarquía y Relaciones de `Persona`
* **Justificación:** En el UML actual, `Persona` es una clase abstracta padre de `Socio` y `Trabajador`. No obstante, aparece una línea secundaria etiquetada *"hereda datos personales"*, lo cual es redundante si ya existe una relación de Herencia UML (`△`).
* **Acción a realizar:**
  1. Eliminar la línea asociativa superflua *"hereda datos personales"*.
  2. Mantener únicamente la flecha de herencia UML hueca (`△`) desde `Socio` hacia `Persona` y desde `Trabajador` hacia `Persona`.

---

## 4. 📐 Diagrama Estructural Propuesto (Visión Corregida)

```
                       ┌─────────────────────────┐
                       │   «abstract» Persona    │
                       ├─────────────────────────┤
                       │ - rut: String           │
                       │ - nombres: String       │
                       │ - apellidoPaterno: String│
                       │ - apellidoMaterno: String│
                       │ - telefono: String      │
                       │ - correoElectronico: Str│
                       ├─────────────────────────┤
                       │ + validarRut(): Boolean │
                       └────────────▲────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
       ┌────────────┴──────────┐       ┌────────────┴──────────┐
       │         Socio         │       │  «abstract» Trabajador│
       ├───────────────────────┤       ├───────────────────────┤
       │ - estadoActivo: Bool  │       │ - idTrabajador: Int   │
       ├───────────────────────┤       │ - passwordHash: String│
       │ + crearFicha(): void  │       ├───────────────────────┤
       │ + tieneMembresia():Bool│      │ + autenticar(): Bool  │
       └───────────────────────┘       └────────────▲──────────┘
                                                    │
                               ┌────────────────────┴────────────────────┐
                               │                                         │
                 ┌─────────────┴─────────────┐             ┌─────────────┴─────────────┐
                 │        Instructor         │             │       Recepcionista       │
                 ├───────────────────────────┤             ├───────────────────────────┤
                 │ - especialidad: String    │             │ - turno: String           │
                 ├───────────────────────────┤             ├───────────────────────────┤
                 │ + dictarClase(): void     │             │ + registrarSocio(): Bool  │
                 │ + marcarAsistencia(): void│             │ + cobrarMensualidad():Bool│
                 └───────────────────────────┘             │ + registrarVenta(): Bool  │
                                                           └───────────────────────────┘
```

---

## 5. ✅ Lista de Chequeo (Checklist) para la Entrega Final

- [ ] ¿Se eliminaron las clases `Direccion`, `Comuna` y `ContactoEmergencia`?
- [ ] ¿Se especificó quién crea y modifica las clases (ej. clase `Administrador`)?
- [ ] ¿La relación entre `DetalleInscripcion` y `Clase` es `*` a `1`?
- [ ] ¿La validación de RUT está asignada a la clase `Persona` o `Socio`?
- [ ] ¿Se mantiene el cálculo de conversión CLP en `Suplemento` con `IndicadorDolar`?
- [ ] ¿Las 3 subclases de `Clase` (`Yoga`, `Spinning`, `Crossfit`) mantienen sus atributos específicos?

---

*Documento preparado para la asignatura de Programación Orientada a Objetos — Proyecto PowerFit.*
