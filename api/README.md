# PowerFit API 2

Esta versión protege las operaciones del gimnasio mediante sesiones y permisos por rol.
La carpeta `api` original no se modifica.

## Instalación

```powershell
python -m pip install -r requirements.txt
```

## Configurar al dueño o administrador inicial

Antes de iniciar la API, define un usuario y una contraseña en variables de entorno.
No escribas estas credenciales dentro de `api.py`.

```powershell
$env:POWERFIT_ADMIN_USUARIO = "dueno"
$env:POWERFIT_ADMIN_PASSWORD = "Usa-una-clave-larga-y-unica"
python -m uvicorn api:app --reload
```

La documentación interactiva estará en `http://127.0.0.1:8000/docs`.

## Iniciar sesión

El dueño o administrador llama a `POST /auth/login`:

```json
{
  "tipo_usuario": "administrador",
  "usuario": "dueno",
  "password": "Usa-una-clave-larga-y-unica"
}
```

Un trabajador registrado utiliza su código:

```json
{
  "tipo_usuario": "trabajador",
  "usuario": "10",
  "password": "clave-del-trabajador"
}
```

La respuesta contiene `access_token`. En las siguientes solicitudes se envía así:

```text
Authorization: Bearer <access_token>
```

En Swagger, pulsa **Authorize** e introduce el token. Las sesiones duran ocho horas y
se eliminan cuando se reinicia el servidor. `POST /auth/logout` invalida la sesión actual.

## Permisos

| Operación | Administrador | Recepcionista | Instructor |
|---|:---:|:---:|:---:|
| Crear y listar trabajadores | Sí | No | No |
| Crear y asignar clases | Sí | No | No |
| Registrar y consultar socios | Sí | Sí | No |
| Inscribir socios | Sí | Sí | No |
| Cobrar y activar socios | Sí | Sí | No |
| Productos, inventario y ventas | Sí | Sí | No |
| Consultar clases | Sí | Sí | Sí |
| Marcar asistencia | No | No | Solo sus clases |
| Realizar una clase | Sí | No | Solo sus clases |

El administrador debe crear primero los trabajadores mediante `POST /trabajadores`.
Después cada trabajador puede iniciar sesión con su `codigo_trabajador`.

## Consideraciones

- Las contraseñas de trabajadores se guardan con PBKDF2 y una sal aleatoria.
- Las contraseñas ya no se envían como parámetros `?pass=`.
- Solo `/`, `/docs` y `/auth/login` son públicos.
- Los datos y las sesiones continúan almacenados en memoria y se pierden al reiniciar.
- Para producción se debe usar una base de datos, HTTPS y un gestor seguro de secretos.
