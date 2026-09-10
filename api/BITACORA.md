# Bitacora del proyecto PowerFit

## Fecha

9 de septiembre de 2026

## 1. Modelado de clases del UML

Se crearon clases Python basadas en `ProyectGym.drawio`, dejando una clase por archivo:

- `Comuna`
- `Venta`
- `MembresiaMensual`
- `DetalleInscripcion`
- `Trabajador`
- `Socio`
- `Yoga`
- `DetalleVenta`
- `ClaseDirigida`
- `Spinning`
- `Suplemento`
- `Inventario`
- `Instructor`
- `Recepcionista`
- `ContactoEmergencia`
- `Crossfit`
- `IndicadorDolar`

Las clases existentes `Persona` y `Direccion` se mantuvieron como base del modelo.

## 2. Mejoras de validacion

- Se implemento la validacion del RUT chileno mediante el algoritmo Modulo 11.
- Se implemento la validacion de telefono.
- Se implemento la validacion de correo electronico.
- Se valido que las edades sean iguales o mayores a 18 anos.
- Se validaron cantidades, precios y stock para evitar valores negativos o cero.
- Se validaron codigos positivos para socios, trabajadores, clases, productos y direcciones.
- Se agrego control de RUT y codigos duplicados.
- Se centralizaron las validaciones de personas en la API para evitar repetir codigo.
- Se agregaron mensajes de error HTTP mas claros.

## 3. Mejoras de socios y clases

- `Socio.crearFicha()` ahora crea una ficha con RUT, nombre completo, contacto de emergencia y observaciones.
- La inscripcion a clases comprueba que el socio exista, este activo y tenga membresia vigente.
- `ClaseDirigida.realizarClase()` verifica que existan socios inscritos antes de marcar la clase como realizada.
- `Yoga`, `Spinning` y `Crossfit` reutilizan la validacion de la clase base.
- Se controlan los cupos generales y los cupos limitados por bicicletas o estaciones.

## 4. API REST

Se creo `api.py` usando FastAPI.

### Socios

- Registrar socios.
- Listar socios.
- Consultar un socio mediante su `rut`.
- Crear automaticamente una membresia inicial de 30 dias.
- Mostrar validaciones y estado de membresia.

### Trabajadores

- Registrar instructores y recepcionistas.
- Usar `codigo_trabajador` como identificador interno.
- Usar `rut` como identificador personal del trabajador.
- Validar contrasena con el parametro `pass`.
- Asignar clases a instructores.
- Registrar asistencia.
- Activar socios desde recepcion.
- Registrar cobros de mensualidad.

### Clases

- Crear clases de Yoga, Spinning y Crossfit.
- Listar clases.
- Inscribir socios usando `codigo_clase` y `rut`.

### Productos, inventario y ventas

- Registrar suplementos mediante `POST /productos`.
- Consultar existencias mediante `GET /inventario`.
- Crear ventas mediante `POST /ventas`.
- Validar que el recepcionista exista y tenga el rol correcto.
- Validar que los productos existan.
- Validar que haya stock suficiente.
- Calcular el precio en CLP usando el valor del dolar.
- Descontar el stock solamente despues de confirmar la venta.
- Informar alertas cuando el stock llega al minimo.

## 5. Nombres de datos

Se normalizaron los nombres publicos de la API usando `snake_case`, por ejemplo:

- `tipo_clase`
- `codigo_clase`
- `nombre_clase`
- `cupo_maximo`
- `codigo_trabajador`
- `codigo_producto`
- `correo_electronico`
- `numero_direccion`

Para socios, las rutas usan `rut` en lugar de `codigo_socio`.

## 6. Documentacion

- Se actualizo `README.md`.
- Se agregaron instrucciones para instalar dependencias.
- Se documentaron las rutas principales.
- Se agregaron ejemplos JSON para socios, trabajadores y clases.
- Se explico el uso de Swagger en `/docs`.

## 7. Comprobaciones realizadas

- Compilacion de todos los archivos Python con `compileall`.
- Revision de errores del proyecto sin diagnosticos pendientes.
- Prueba de validacion de RUT, telefono y correo.
- Prueba de membresia y cupos de clases.
- Prueba de calculo de ventas.
- Prueba de descuento de stock.
- Prueba de alertas de inventario.

## 8. Limitaciones pendientes

- Los datos se almacenan en memoria y se pierden al reiniciar la API.
- La API todavia deberia usar una base de datos como SQLite o PostgreSQL.
- La contrasena se guarda como hash SHA-256; para produccion conviene usar bcrypt o Argon2.
- Todavia se pueden agregar pruebas automaticas con pytest.
- La API y el dominio podrian separarse en carpetas para facilitar el mantenimiento.

## 9. Mejoras confirmadas

Comprobe que se corrigieron varios problemas de la auditoria anterior:

- Spinning ya respeta el numero de bicicletas.
- CrossFit ya respeta el numero de estaciones.
- Probe una clase con dos bicicletas: acepto dos socios y rechazo al tercero correctamente.
- `DetalleVenta` ahora conserva `codigoProducto`.
- La respuesta de una venta muestra el codigo del producto.
- El RUT se normaliza al registrar socios y trabajadores.
- La asistencia ahora se relaciona con una clase concreta.
- Se verifica que el instructor sea quien dicta la clase.
- Se verifica que el socio este inscrito y tenga membresia vigente.
- Se impide inscribir personas en una clase ya realizada.
- El cobro de mensualidad ahora intenta renovar la membresia.

Las correcciones principales estan en [api.py](C:/Users/jarri/Desktop/PowerFit/api/api.py), [spinning.py](C:/Users/jarri/Desktop/PowerFit/api/spinning.py), [crossfit.py](C:/Users/jarri/Desktop/PowerFit/api/crossfit.py) y [detalle_venta.py](C:/Users/jarri/Desktop/PowerFit/api/detalle_venta.py).
