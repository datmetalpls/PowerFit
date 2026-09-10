# Guia explicada de PowerFit

Esta guia explica el proyecto desde lo general hasta cada clase y metodo. Las lineas que aparecen juntas normalmente pertenecen al mismo bloque y cumplen una sola responsabilidad.

## 1. Como esta organizado el proyecto

- `persona.py`: clase base para cualquier persona.
- `direccion.py`: domicilio de una persona.
- `socio.py`: persona que usa el gimnasio.
- `trabajador.py`: persona que trabaja en el gimnasio.
- `instructor.py`: trabajador que dirige clases.
- `recepcionista.py`: trabajador que atiende socios y ventas.
- `clase_dirigida.py`: clase base para Yoga, Spinning y Crossfit.
- `yoga.py`, `spinning.py`, `crossfit.py`: especializaciones de clases.
- `membresia_mensual.py`: período de acceso de un socio.
- `detalle_inscripcion.py`: reserva individual.
- `suplemento.py`: producto vendido.
- `inventario.py`: control de stock.
- `detalle_venta.py`: una línea de una venta.
- `venta.py`: venta completa.
- `api.py`: acceso REST a las clases mediante FastAPI.
- `main.py`: ejemplo de uso por consola.
- `README.md`: instrucciones rápidas.
- `BITACORA.md`: historial de cambios.

La idea principal es que las clases del dominio contienen las reglas del gimnasio y la API solo recibe datos, valida y llama a esas clases.

## 2. Persona

### Importaciones

`import re` permite validar teléfono y correo con expresiones regulares.

`from direccion import Direccion` permite indicar que cada persona tiene una dirección.

### Atributos

`rut` identifica legalmente a la persona. Se usa como dato inmutable porque cambiarlo podría mezclar historiales.

`edad`, `nombres`, `apellidoPaterno` y `apellidoMaterno` representan la identidad de la persona.

`telefono` y `correoElectronico` son datos de contacto y pueden cambiar.

`_rut`, `_telefono`, etc. usan guion bajo para indicar que son atributos internos. Python no los vuelve privados de forma absoluta; es una convención de encapsulamiento.

### Constructor `__init__`

El constructor recibe todos los datos obligatorios y los guarda en atributos internos. Se usa un constructor explícito para que sea claro qué necesita una persona.

La dirección se guarda como objeto, no como texto. Esto permite usar métodos como `getCalle()` y mantener la responsabilidad de la dirección en `Direccion`.

### Getters

`getRut()`, `getEdad()`, `getNombres()`, `getApellidoPaterno()`, `getApellidoMaterno()`, `getTelefono()`, `getCorreoElectronico()` y `getDireccion()` devuelven los datos sin acceder directamente a los atributos internos.

La razón es centralizar la lectura y poder cambiar la implementación interna sin cambiar el código que usa la clase.

### Setters

`setTelefono()` y `setCorreoElectronico()` permiten actualizar datos que naturalmente pueden cambiar.

`setDireccion()` permite cambiar de domicilio.

No existe setter para el RUT ni para los nombres porque en el diseño se consideran datos de identidad.

### `validarRut()`

1. Comprueba que exista un texto.
2. Quita puntos, guiones y espacios.
3. Separa el cuerpo numérico del dígito verificador.
4. Recorre el cuerpo desde derecha a izquierda.
5. Multiplica cada dígito por la secuencia del Módulo 11.
6. Calcula el dígito esperado.
7. Compara el resultado con el dígito ingresado.

Se usa Módulo 11 porque es el algoritmo de validación del RUT chileno. No basta comprobar que el RUT tenga números: también debe tener un dígito verificador correcto.

### `validarTelefono()`

Quita caracteres que no sean números y acepta una cantidad razonable de dígitos. Así permite formatos como `+56 9 1234 5678` sin guardar reglas innecesariamente complejas.

### `validarCorreoElectronico()`

Usa una expresión regular sencilla para exigir texto antes de `@`, un dominio y un punto. Es una validación de formato, no verifica que el correo exista.

## 3. Direccion

`Direccion` guarda `idDireccion`, tipo, calle, número y referencia.

`TIPOS_DIRECCION` limita los tipos aceptados a `casa`, `dpto` y `block`. Se usa una lista para evitar valores escritos de forma diferente.

El constructor limpia el tipo con `strip()` y `lower()`. Luego rechaza cualquier valor no permitido con `ValueError`.

Los getters devuelven cada parte de la dirección.

Los setters permiten cambiar tipo, calle, número y referencia. El identificador no tiene setter porque identifica el registro y no debería cambiar.

## 4. Socio

`Socio` hereda de `Persona` porque un socio es una persona con información adicional.

El constructor llama a `super().__init__()` para reutilizar la creación de los datos personales. Luego agrega:

- `estadoActivo`: indica si puede usar el gimnasio.
- `membresias`: lista de membresías del socio.

### `crearFicha()`

Crea un diccionario con RUT, nombre completo, contacto de emergencia y observaciones. Antes solo era un diccionario vacío; ahora deja una estructura útil para futuras funciones.

Se comprueba `hasattr()` para no reemplazar una ficha ya existente.

### `tieneMembresiaVigente()`

Devuelve verdadero solo si el socio está activo y alguna membresía está vigente. Se usa `any()` porque basta encontrar una membresía válida.

## 5. MembresiaMensual

Guarda fecha de inicio, fecha de término y estado vigente.

### `esVigente()`

Usa la fecha recibida o la fecha actual. Comprueba que la fecha esté dentro del intervalo y que el estado sea activo.

### `renovar()`

Recibe una cantidad de meses, calcula el nuevo año y mes y respeta la cantidad real de días del mes. Esto es mejor que sumar siempre 30 días, porque febrero y otros meses no duran lo mismo.

## 6. Trabajador

`Trabajador` hereda de `Persona` porque también tiene identidad, contacto y dirección.

El constructor agrega:

- `idTrabajador`: código interno del trabajador.
- `passHash`: contraseña guardada como hash.
- `permisos`: conjunto de acciones permitidas.

### `autenticar()`

Compara el hash recibido con el almacenado. La API convierte primero la contraseña escrita a hash.

### `cambiarPassword()`

Reemplaza el hash guardado. En una aplicación real se debería comprobar la contraseña anterior y aplicar bcrypt o Argon2.

### `tienePermiso()`

Pregunta si un permiso está en el conjunto. Un conjunto evita duplicados y hace eficiente la búsqueda.

## 7. Instructor

`Instructor` hereda de `Trabajador` y agrega `especialidad`.

### `dictarClase(clase)`

Guarda el instructor dentro de la clase. Así se puede saber quién dirige la actividad.

### `marcarAsistencia(socio)`

Crea una lista de asistencias si aún no existe y agrega al socio solo si no estaba registrado. La comprobación evita duplicar asistencias.

## 8. Recepcionista

`Recepcionista` hereda de `Trabajador` y agrega `turno`.

### `registrarSocio(socio)`

Activa el socio y devuelve `True`. Esto representa la operación de habilitarlo desde recepción.

### `cobrarMensualidad(socio)`

Rechaza socios inactivos y marca la mensualidad como cobrada. En una versión completa debería crear un comprobante y extender la membresía.

### `registrarVenta(venta)`

Rechaza ventas vacías, revisa el stock de cada detalle y exige que el total sea mayor que cero. La función devuelve `False` cuando la venta no es válida para que la API pueda responder con un error claro.

## 9. ClaseDirigida

Es la clase base de las actividades. Guarda código, nombre, cupo máximo, duración, socios inscritos y estado de realización.

### `calcularCuposDisponibles()`

Resta los socios inscritos al cupo máximo. `max(0, ...)` evita mostrar un número negativo.

### `capacidadExtraDisponible()`

Devuelve la capacidad calculada y sirve como punto de extensión para clases con equipamiento limitado.

### `hayCupo()`

Devuelve verdadero cuando queda espacio.

### `inscribirSocio()`

No permite sobrepasar la capacidad ni inscribir al mismo objeto dos veces.

### `realizarClase()`

No permite marcar una clase sin inscritos. Si existe al menos un socio, cambia `realizada` a `True`.

## 10. Yoga, Spinning y Crossfit

Las tres clases heredan de `ClaseDirigida` para reutilizar código.

### Yoga

Agrega `nivel`, porque una clase de Yoga puede ser inicial, intermedia o avanzada.

`calcularCuposDisponibles()` reutiliza el cálculo de la clase base.

`realizarClase()` llama a `super()` para aplicar la regla de no realizar clases vacías.

### Spinning

Agrega `bicicletasDisponibles`.

El cálculo de cupos usa el menor valor entre el cupo general y las bicicletas disponibles. No se puede aceptar a más personas que bicicletas.

### Crossfit

Funciona igual que Spinning, pero usa `estacionesDisponibles` para limitar la capacidad real.

## 11. DetalleInscripcion

Representa una reserva con identificador, día de la semana y estado reservado.

`reservar()` devuelve `False` si ya estaba reservada. Si no, cambia el estado y devuelve `True`.

`cancelar()` libera la reserva y permite que el cupo vuelva a estar disponible.

## 12. ContactoEmergencia

Guarda identificador, nombre, parentesco y teléfono de una persona a contactar.

`validarTelefono()` elimina separadores y comprueba una cantidad razonable de dígitos. Se usa una expresión regular para aceptar teléfonos escritos con espacios o símbolos.

## 13. Suplemento

Representa un producto con código, nombre, stock y precio en dólares.

El constructor rechaza stock o precios negativos.

`hayStock()` comprueba si queda al menos una unidad.

`descontarStock()` valida que la cantidad sea positiva y que exista stock suficiente antes de descontar.

`calcularPrecioCLP()` multiplica el precio en dólares por el valor del dólar. Se usa `Decimal` para evitar errores típicos de los números decimales binarios.

## 14. Inventario

Guarda fecha de actualización, stock mínimo y stock actual.

El constructor rechaza valores negativos.

`reponerStock()` suma unidades y actualiza la fecha.

`alertaStock()` devuelve verdadero si el stock actual está en el mínimo o por debajo. Así la recepción puede saber cuándo comprar más.

## 15. DetalleVenta

Representa una línea de venta.

Guarda cantidad, precio unitario, stock disponible y subtotal.

El constructor rechaza cantidades no positivas, precios negativos y stock negativo.

`calcularSubtotal()` multiplica cantidad por precio unitario.

`confirmarStock()` comprueba si las unidades disponibles alcanzan para la venta.

## 16. Venta

Agrupa varios `DetalleVenta`.

`agregarDetalle()` rechaza detalles inexistentes o sin stock, agrega el detalle y recalcula el total.

`calcularTotal()` suma todos los subtotales usando `Decimal("0")` como valor inicial. Esto evita iniciar la suma con un entero y mantiene el tipo monetario.

## 17. IndicadorDolar

Guarda la fecha y el valor del dólar en CLP.

El constructor y `actualizarValor()` rechazan valores menores o iguales a cero.

`obtenerValor()` devuelve el valor vigente.

`actualizarValor()` reemplaza el valor y actualiza la fecha para dejar trazabilidad.

## 18. Comuna

Guarda código, nombre y estado activo.

`registrar()` activa una comuna.

`actualizar()` cambia su nombre.

`desactivar()` la marca como inactiva sin eliminar el registro histórico.

## 19. API FastAPI

### Imports y aplicación

`FastAPI` crea la aplicación web.

`HTTPException` permite responder errores HTTP claros, por ejemplo `404` cuando no existe un socio.

`Query` define datos enviados en la URL, como `pass`.

`BaseModel` y `Field` de Pydantic validan automáticamente los JSON recibidos.

Los diccionarios `socios`, `clases`, `trabajadores`, `productos`, `inventarios` y `ventas` funcionan como almacenamiento temporal en memoria. Las claves permiten buscar rápidamente cada objeto.

### Modelos de entrada

`DireccionEntrada` describe los datos del domicilio.

`SocioEntrada` describe el JSON para registrar un socio y usa `rut`, no `codigo_socio`.

`ClaseEntrada` usa nombres como `codigo_clase`, `nombre_clase`, `cupo_maximo` y `duracion_minutos` para que Swagger explique qué dato se espera.

`TrabajadorEntrada` recibe tipo, código interno, RUT, contraseña y datos personales.

`ProductoEntrada`, `DetalleVentaEntrada` y `VentaEntrada` describen productos y ventas.

`Field(gt=0)`, `Field(ge=0)` y `Field(min_length=1)` evitan datos imposibles antes de llegar al dominio.

### Funciones de conversión

`convertir_socio_a_respuesta()` transforma un objeto Python en un diccionario JSON y evita exponer atributos internos.

`convertir_clase_a_respuesta()` informa cupos, duración, tipo y socios inscritos.

`convertir_trabajador_a_respuesta()` nunca devuelve `passHash`.

Las funciones de conversión separan el modelo interno del formato público de la API.

### Validación y autenticación

`crear_hash()` transforma la contraseña antes de almacenarla. Para producción se recomienda bcrypt o Argon2 porque SHA-256 solo no es un algoritmo especializado para contraseñas.

`validar_datos_persona()` centraliza RUT, teléfono y correo. Así socios y trabajadores usan las mismas reglas.

`obtener_trabajador_autorizado()` busca por código interno y comprueba la contraseña.

`exigir_rol()` comprueba que el trabajador sea Instructor o Recepcionista según la operación.

### Rutas

`GET /` confirma que la API está funcionando.

`POST /socios` valida el JSON, crea la dirección, crea el socio y agrega una membresía inicial.

`GET /socios` devuelve todos los socios.

`GET /socios/{rut}` busca un socio por su RUT.

`POST /trabajadores` crea un instructor o recepcionista y asigna permisos según el tipo.

`GET /trabajadores` devuelve trabajadores sin contraseñas.

`POST /instructores/{codigo_trabajador}/clases/{codigo_clase}` asigna una clase a un instructor autenticado.

`POST /instructores/{codigo_trabajador}/asistencias/{rut}` registra asistencia.

`POST /recepcionistas/{codigo_trabajador}/socios/{rut}/activar` activa un socio.

`POST /recepcionistas/{codigo_trabajador}/socios/{rut}/cobrar` registra el cobro.

`POST /productos` registra un suplemento y su inventario inicial.

`GET /inventario` muestra stock actual, mínimo y alerta.

`POST /ventas` verifica recepcionista, producto, stock y valor del dólar; luego calcula la venta y descuenta existencias.

`POST /clases` crea Yoga, Spinning o Crossfit según `tipo_clase`.

`GET /clases` lista las clases.

`POST /clases/{codigo_clase}/inscripciones/{rut}` comprueba existencia, actividad, membresía y cupos antes de inscribir.

## 20. Main de consola

`main.py` es una demostración sin servidor.

Las funciones `pedir_texto()`, `pedir_entero()`, `pedir_edad()`, `pedir_rut()` y `pedir_tipo_direccion()` repiten la entrada hasta recibir datos válidos.

`ingresar_direccion()` crea una dirección desde la consola.

`ingresar_socio()` crea un socio usando esa dirección.

`mostrar_socio()` imprime datos personales, dirección y membresía.

`main()` crea una membresía, crea una clase de Yoga e inscribe al socio.

El bloque `if __name__ == "__main__"` evita que la demostración se ejecute cuando `main.py` se importa desde otro archivo.

## 21. Archivos experimentales de PowerFit

`PowerFit/primer.py` es una demostración independiente de Protocol, dataclass, inyección de dependencias y una salida animada.

`PowerFit/arch.py`, `PowerFit/test.py` y `PowerFit/roro.py` son archivos de prueba o demostración y no forman parte de la API principal.

`PowerFit/persona.py` es un borrador mínimo de Persona. La versión real que usa el proyecto es la Persona de la raíz.

## 22. Ideas importantes para entender el diseño

- La herencia evita repetir los datos comunes de Persona y Trabajador.
- La composición permite que una Persona tenga una Direccion y que una Venta tenga DetalleVenta.
- Las listas representan relaciones de uno a muchos, como un socio con varias membresías.
- Los diccionarios de la API permiten buscar por código o RUT.
- Los modelos Pydantic validan la entrada HTTP.
- Las clases del dominio contienen reglas; la API coordina entradas y respuestas.
- Los comentarios explican intención y motivo, no solo traducen literalmente cada instrucción.
