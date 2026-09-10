# PowerFit

## API

La API REST está en `api.py` y utiliza FastAPI. Para instalar sus dependencias:

```powershell
python -m pip install -r requirements.txt
```

Para iniciar el servidor:

```powershell
python -m uvicorn api:app --reload
```

La documentación interactiva queda disponible en:

```text
http://127.0.0.1:8000/docs
```

Endpoints principales:

- `POST /socios`: registrar un socio.
- `GET /socios`: listar socios.
- `GET /socios/{rut}`: consultar un socio usando su RUT.
- `POST /socios/{rut}/ficha`: crear la ficha de seguimiento del socio.
- `POST /clases`: crear una clase de Yoga, Spinning o Crossfit.
- `GET /clases`: listar clases.
- `POST /clases/{codigo_clase}/realizar`: marcar una clase como realizada.
- `POST /clases/{codigo_clase}/inscripciones/{rut}`: inscribir un socio.
- `POST /trabajadores`: registrar un instructor o recepcionista.
- `GET /trabajadores`: listar trabajadores sin contraseñas.
- `POST /instructores/{codigo_trabajador}/clases/{codigo_clase}?pass=...`: asignar una clase.
- `POST /instructores/{codigo_trabajador}/asistencias/{rut}?pass=...`: marcar asistencia.
- `POST /recepcionistas/{codigo_trabajador}/socios/{rut}/activar?pass=...`: activar un socio.
- `POST /recepcionistas/{codigo_trabajador}/socios/{rut}/cobrar?pass=...`: registrar un cobro.
- `POST /productos`: registrar un suplemento.
- `GET /inventario`: consultar existencias y alertas.
- `POST /ventas?codigo_trabajador=1&pass=...`: registrar una venta y descontar stock.

Los endpoints de trabajadores reciben la contraseña directamente mediante el parámetro `pass`.

Las contraseñas se almacenan como hash y no se devuelven en las respuestas.

Ejemplo de datos para `POST /clases`:

```json
{
	"tipo_clase": "yoga",
	"codigo_clase": 101,
	"nombre_clase": "Yoga inicial",
	"cupo_maximo": 15,
	"duracion_minutos": 60,
	"nivel": "Inicial"
}
```

Ejemplo de datos para `POST /socios`:

```json
{
	"rut": "12.345.678-5",
	"edad": 25,
	"nombres": "Ana",
	"apellido_paterno": "Perez",
	"apellido_materno": "Lopez",
	"telefono": "987654321",
	"correo_electronico": "ana@example.com",
	"direccion": {
		"codigo_direccion": 1,
		"tipo_direccion": "casa",
		"calle": "Avenida Uno",
		"numero_direccion": "123",
		"referencia": "Centro"
	}
}
```

Para `POST /trabajadores`, usa `codigo_trabajador` para identificar al trabajador:

```json
{
	"tipo_trabajador": "instructor",
	"codigo_trabajador": 1,
	"rut": "11.111.111-1",
	"pass": "clave123",
	"edad": 30,
	"nombres": "Carlos",
	"apellido_paterno": "Gomez",
	"apellido_materno": "Soto",
	"telefono": "912345678",
	"correo_electronico": "carlos@example.com",
	"especialidad": "Yoga",
	"direccion": {
		"codigo_direccion": 2,
		"tipo_direccion": "casa",
		"calle": "Avenida Dos",
		"numero_direccion": "456",
		"referencia": "Norte"
	}
}
```

Los datos se almacenan en memoria y se pierden al reiniciar el servidor.
