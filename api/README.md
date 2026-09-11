# PowerFit API 2

Esta versión protege las operaciones del gimnasio mediante autenticación Basic y permisos por rol.
La carpeta `api` original no se modifica.

## Instalación

```powershell
python -m pip install -r requirements.txt
```

## Administrador inicial

La clase `Admin` contiene el identificador fijo `17310447-2` y valida la contraseña
`pelusita00` contra un hash PBKDF2. El administrador debe crear primero a los trabajadores.

```powershell
python -m uvicorn api:app --reload
```

La documentación interactiva estará en `http://127.0.0.1:8000/docs`.

## Credenciales por solicitud

No existe login, logout ni token. Cada operación privada debe incluir credenciales HTTP Basic.
El administrador usa su identificador y clave fija:

```text
Authorization: Basic base64(17310447-2:pelusita00)
```

Cada trabajador usa como usuario su `codigo_trabajador` y la contraseña asignada por el
administrador al registrarlo:

```text
Authorization: Basic base64(10:clave-del-trabajador)
```

En Swagger, pulsa **Authorize** e introduce usuario y contraseña en el cuadro Basic Auth.

## Permisos

| Operación | Administrador | Recepcionista | Instructor |
|---|:---:|:---:|:---:|
| Crear y listar trabajadores | Sí | No | No |
| Crear y asignar clases | Sí | No | No |
| Registrar y consultar socios | No | Sí | No |
| Inscribir socios | No | No | Sí |
| Cobrar y activar socios | Sí | Sí | No |
| Productos e inventario | Sí | Sí | No |
| Registrar ventas | No | Sí | No |
| Consultar clases | Sí | Sí | Sí |
| Marcar asistencia | No | No | Solo sus clases |
| Realizar una clase | Sí | No | Solo sus clases |

El administrador debe crear primero los trabajadores mediante `POST /trabajadores`.
Después cada trabajador puede acceder directamente usando su `codigo_trabajador` y contraseña.

## Consideraciones

- Las contraseñas de trabajadores se guardan con PBKDF2 y una sal aleatoria.
- Las contraseñas ya no se envían como parámetros `?pass=`.
- Solo `/` y `/docs` son públicos.
- Los datos continúan almacenados en memoria y se pierden al reiniciar.
- Para producción se debe usar una base de datos, HTTPS y un gestor seguro de secretos.
