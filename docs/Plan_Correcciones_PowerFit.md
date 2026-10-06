# Plan de Acción y Correcciones PowerFit

A continuación, se detalla el diagnóstico y la propuesta técnica para cada uno de los puntos reportados. Por favor, revisa este documento y confirma si estás de acuerdo antes de que proceda a aplicar los cambios en el código.

---

## 1. Datos de dirección particular en el módulo de Socios
- **Problema detectado:** El formulario de la interfaz gráfica captura el tipo de vivienda y la comuna, y se crea el objeto POO `Direccion`, pero el `SocioDAO` ignora completamente estos datos. La tabla `socios` en la base de datos (SQLite) no cuenta con columnas para almacenar la dirección.
- **Comportamiento esperado:** La dirección (calle, número, comuna, tipo de vivienda) debe guardarse en la base de datos al registrar un Socio y recuperarse al cargar.
- **Resultado actual:** La dirección ingresada se pierde al cerrar la aplicación (solo vive en memoria RAM).
- **Propuesta de corrección:** 
  1. Añadir columnas `dir_calle`, `dir_numero`, `dir_comuna`, `dir_tipo` a la tabla `socios` en `src/dao/conexion.py` (usando `ALTER TABLE` para retrocompatibilidad).
  2. Modificar el CRUD de `src/dao/socio_dao.py` para inyectar y recuperar estos campos de SQLite.

---

## 2. Persistencia de información en el módulo de Salas
- **Problema detectado:** La tabla `clases` guarda la clase, pero no registra explícitamente el "Tipo de Disciplina" (Yoga, Spinning, Crossfit) ni la cantidad de recursos físicos (colchonetas, bicicletas, estaciones). El DAO intenta inferir el tipo usando `.lower()` sobre el nombre de la clase.
- **Comportamiento esperado:** Los recursos físicos y el tipo de clase deben persistir explícitamente para garantizar que el polimorfismo de cupos no falle si alguien le cambia el nombre a la clase.
- **Resultado actual:** Variables específicas (`colchonetas`, `bicicletas`) no se guardan y al cargar se igualan al `cupo_maximo` por defecto.
- **Propuesta de corrección:** 
  1. Agregar columnas `tipo_disciplina` (TEXT) y `recurso_fisico` (INTEGER) a la tabla `clases` en la base de datos.
  2. Actualizar `clase_dao.py` para mapear los recursos reales (ej. `_colchonetas`) a esta nueva columna en la BD.

---

## 3. Manejo y visualización de precios en dólares
- **Problema detectado:** El precio de los suplementos depende del dólar del día, pero el valor histórico en dólares no queda guardado.
- **Comportamiento esperado:** Al revisar el historial de ventas, el administrador debería poder ver cuánto costaba el producto en dólares y con qué tasa de cambio (CLP) se procesó.
- **Resultado actual:** La tabla `ventas` solo guarda el total en pesos chilenos (`total_clp`). 
- **Propuesta de corrección:** 
  1. Agregar columna `tasa_cambio_usd` a la tabla `ventas` en la BD.
  2. Modificar `VentaDAO` para guardar el valor del dólar actual en la transacción.
  3. Mostrar una nueva columna `Precio (USD)` o `Valor Dólar (Día)` en la tabla `QTableWidget` de ventas en la interfaz.

---

## 4. Persistencia de datos en el proceso de Venta
- **Problema detectado:** Cuando se procesa una venta, el `VentaDAO` la guarda en la tabla `ventas` y `detalles_ventas`, pero nunca descuenta el inventario físico de la tabla `suplementos`.
- **Comportamiento esperado:** Al vender un producto, su `stock` en la base de datos debe disminuir.
- **Resultado actual:** El inventario solo baja en la memoria (POO), pero al reiniciar el programa el inventario en la BD sigue intacto.
- **Propuesta de corrección:** En el método `VentaDAO.guardar()`, añadir un `UPDATE suplementos SET stock = stock - ? WHERE id_suplemento = ?` que se ejecute dentro de la misma transacción (para evitar ventas fantasma).

---

## 5. Separación y visualización de apellido paterno y materno en Personas
- **Problema detectado:** El formulario de la interfaz gráfica tiene un único input para ambos apellidos (`input_apellidos`), enviando todo el texto a la variable `apellidoPaterno` y dejando `apellidoMaterno` vacío en la base de datos.
- **Comportamiento esperado:** Formularios con campos separados y tablas que concatenen correctamente ambos en la vista.
- **Resultado actual:** La tabla de base de datos tiene las columnas listas, pero el Front-End (PySide6) las omite.
- **Propuesta de corrección:** Duplicar el input en la GUI (`input_apellido_paterno` e `input_apellido_materno`) para el módulo de Socios y Personal. Ajustar el paso de parámetros en el registro.

---

## 6. Métodos de inscripción y cantidad de reservas
- **Problema detectado:** En la GUI, el panel inscribe al socio al hacer clic en un asiento. Sin embargo, no existe un flujo para "Agregar una nueva clase" (Crear nuevos horarios en la BD) y un socio puede inscribirse de forma extraña en la matriz POO ocupando múltiples asientos, aunque en BD el `UNIQUE(id_socio, id_clase)` lo restrinja silenciosamente.
- **Comportamiento esperado:** Debería existir un límite claro: un socio solo puede reservar un cupo por clase. Además, debería ser posible agregar nuevas clases (horarios).
- **Resultado actual:** Se pueden hacer clics múltiples en los asientos para el mismo socio. No hay formulario para crear clases nuevas.
- **Propuesta de corrección:** 
  1. Validar en `app_window.py` que si el socio seleccionado ya está en `clase.cupos`, se lance una advertencia impidiendo que ocupe dos asientos.
  2. Evaluar agregar un botón "Crear Nueva Clase" que inserte en la base de datos si el rol es Administrador.

---

## 7. Validar bloqueo de contraseña después de 3 intentos fallidos
- **Problema detectado:** No hay límite de reintentos en el Login. Un usuario puede equivocarse infinitas veces.
- **Comportamiento esperado:** Si el usuario falla 3 veces la clave, el sistema debe bloquear el input o cerrarse por seguridad, advirtiendo de la situación.
- **Resultado actual:** `autenticar()` solo retorna booleano, y la GUI permite bucle infinito.
- **Propuesta de corrección:** Añadir un contador `self.intentos_login = 0` en `VentanaRegistro`. Tras 3 fallos consecutivos, deshabilitar el botón de `Acceder` o cerrar la aplicación.

---

## 8. Actualizar configuración de timeout de la API de dólar a 5 segundos
- **Problema detectado:** La API en `suplemento.py` tiene un `timeout=3`.
- **Comportamiento esperado:** El timeout debe ser de 5 segundos. 
- **Resultado actual:** Está en 3 segundos (`timeout=3`). 
- **Impacto (Revisión):** Aumentar a 5 segundos mejora la resiliencia si la API oficial del gobierno chileno `mindicador.cl` responde lento. Sin embargo, si la API se cae por completo, el punto de venta de PowerFit tardará 2 segundos adicionales (5 en total) en arrojar el error interno y aplicar el "Fallback" de $950 CLP. Es un costo de latencia aceptable para aumentar la precisión en caso de tráfico lento.
- **Propuesta de corrección:** Cambiar `urllib.request.urlopen(req, timeout=3)` a `timeout=5`.

---
> **[!] ACCIÓN REQUERIDA:** Por favor, confirma si estás de acuerdo con este plan de acción para que comience a refactorizar el código de inmediato.
