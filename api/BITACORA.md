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
- En `api2`, las contraseñas de trabajadores se protegen con PBKDF2 y sal aleatoria;
  para producción se recomienda migrar a Argon2id.
- Todavia se pueden agregar pruebas automaticas con pytest.
- La API y el dominio podrian separarse en carpetas para facilitar el mantenimiento.

## Actualizaciones - 10 de septiembre de 2026

### Mejoras confirmadas

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

## API 2 - Control de acceso

**Fecha:** 10 de septiembre de 2026  
**Hora:** 14:31:53  
**Zona horaria:** America/Santiago (UTC-03:00)

### Objetivo del cambio

Impedir que personas sin autenticación puedan registrar socios, crear trabajadores,
crear clases o ejecutar otras operaciones internas de PowerFit.

### Cambios realizados

Se creó una copia independiente del proyecto llamada `api2`. En esta versión:

- El administrador inicial usa el identificador fijo `17310447-2` y una contraseña PBKDF2
  con hash fijo almacenado en la clase `Admin`.
- No existen endpoints de login/logout ni tokens.
- Las operaciones privadas requieren credenciales HTTP Basic en cada solicitud.
- Solo el administrador puede registrar y listar trabajadores, crear clases y asignar
  instructores.
- La recepcionista puede registrar socios, gestionar cobros, consultar inventario y registrar
  ventas.
- El instructor puede inscribir socios, marcar asistencia y operar solamente las clases que
  tiene asignadas.
- Las contraseñas dejaron de viajar en parámetros de URL.
- Las contraseñas de trabajadores se protegen con PBKDF2, sal aleatoria y comparación
  segura.
- Se normaliza el RUT en todas las rutas de búsqueda de socios.

### Comprobaciones realizadas

- La aplicación FastAPI se importó correctamente y expuso 24 rutas.
- Se verificaron operaciones protegidas mediante autenticación Basic por solicitud.
- La única operación de negocio pública es el estado de la API.
- Una solicitud anónima para crear socios, trabajadores o clases devuelve HTTP `401`.
- El administrador puede autenticarse y registrar una recepcionista.
- La recepcionista registrada puede autenticarse y registrar un socio.
- Una recepcionista que intenta crear trabajadores o clases recibe HTTP `403`.
- La consulta anónima del listado de socios devuelve HTTP `401`.
- La búsqueda de un socio funciona aunque el RUT se escriba con puntos y guion.
- Se comprobó la sintaxis de los 21 archivos Python.

### Archivos actualizados

- `api2/api.py`
- `api2/README.md`
- `api2/BITACORA.md`

### Limitaciones que permanecen

- Los usuarios y datos continúan almacenados en memoria y desaparecen al reiniciar el servidor.
- Para producción todavía se requiere base de datos, HTTPS, gestión externa de secretos
  y un registro persistente de auditoría.

## Actualizaciones - 11 de septiembre de 2026

### Autenticación y administrador

- Se creó `admin.py` con la clase `Admin`.
- Se estableció el identificador fijo del administrador: `17310447-2`.
- La contraseña administrativa `pelusita00` no se guarda en texto plano; se valida contra
  un hash PBKDF2 con sal fija.
- Se eliminaron los endpoints de login y logout.
- Se eliminaron los tokens Bearer y el almacenamiento de sesiones temporales.
- Se implementó autenticación HTTP Basic por solicitud para administrador y trabajadores.
- El trabajador se autentica usando su `codigo_trabajador` y la contraseña asignada por
  el administrador al registrarlo.

### Bloqueo global de la API

- Se agregó un middleware que exige credenciales HTTP Basic antes de procesar cualquier
  solicitud.
- También quedan protegidos el estado de la API, Swagger, ReDoc y el esquema OpenAPI.
- Las solicitudes sin credenciales reciben HTTP `401`.
- Las credenciales válidas pero sin el rol requerido reciben HTTP `403`.

### Permisos por rol

- El administrador puede crear y listar trabajadores, crear clases y asignar instructores.
- La recepcionista puede registrar socios, activar socios, cobrar mensualidades, consultar
  inventario y registrar ventas.
- El instructor puede inscribir socios, marcar asistencia y realizar sus clases asignadas.
- El administrador ya no puede registrar socios directamente.
- El instructor ya no puede registrar socios ni realizar ventas.
- La inscripción de socios a clases quedó restringida al rol instructor.
- El registro de ventas quedó restringido al rol recepcionista.

### Corrección y comprobaciones

- Se corrigió el import de `get_authorization_scheme_param` para compatibilidad con la
  versión instalada de FastAPI.
- Se comprobó la autenticación correcta e incorrecta del administrador.
- Se comprobó que no existen rutas `/auth/login` ni `/auth/logout`.
- Se comprobó la compilación de todos los módulos con `python -m compileall`.
- Se revisó el archivo `api.py` con los diagnósticos del editor y no quedaron errores.
- Se inició Uvicorn correctamente en `http://127.0.0.1:8001`.

### Documentación actualizada

- Se actualizó `README.md` con el uso de HTTP Basic, las credenciales iniciales y la
  matriz de permisos por rol.
- Se actualizó esta bitácora para reflejar la implementación actual en `api/`.
