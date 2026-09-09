# Importa expresiones regulares para validar el formato del RUT.
import re
# Importa fechas para crear la membresía inicial del socio.
from datetime import date, timedelta

# Importa la clase que representa la dirección del socio.
from direccion import Direccion
# Importa la clase que representa la membresía mensual.
from membresia_mensual import MembresiaMensual
# Importa la clase que representa al socio registrado.
from socio import Socio
# Importa una clase dirigida de ejemplo para la demostración.
from yoga import Yoga


def pedir_texto(mensaje: str) -> str:
    """Solicita un texto no vacío."""
    # Repite la solicitud hasta que el usuario escriba algún valor.
    while True:
        # Lee el texto y elimina espacios innecesarios en los extremos.
        valor = input(mensaje).strip()
        # Devuelve el texto cuando no está vacío.
        if valor:
            return valor
        # Informa al usuario por qué debe intentarlo nuevamente.
        print("El campo no puede quedar vacío.")


def pedir_entero(mensaje: str) -> int:
    """Solicita un número entero válido."""
    # Repite la solicitud hasta recibir un número entero.
    while True:
        try:
            # Convierte la respuesta escrita en un número entero.
            return int(input(mensaje).strip())
        except ValueError:
            # Informa que la conversión no fue posible.
            print("Ingresa un número entero válido.")


def pedir_edad() -> int:
    """Solicita una edad válida para registrar al usuario."""
    # Repite la solicitud hasta cumplir la edad mínima del sistema.
    while True:
        # Pide la edad usando la validación de números enteros.
        edad = pedir_entero("Edad: ")
        # Acepta solamente personas mayores de edad.
        if edad >= 18:
            return edad
        # Rechaza edades menores a 18 años.
        print("El usuario debe ser mayor o igual a 18 años.")


def verificar_rut(rut: str) -> bool:
    """Verifica un RUT chileno usando el algoritmo de Módulo 11."""
    # Elimina puntos, guiones y espacios para revisar solo los caracteres útiles.
    rut_limpio = rut.replace(".", "").replace("-", "").replace(" ", "").upper()

    # Comprueba que exista un cuerpo numérico y un dígito verificador.
    if not re.fullmatch(r"\d+[0-9K]", rut_limpio):
        return False

    # Separa el cuerpo numérico del dígito verificador.
    cuerpo = rut_limpio[:-1]
    digito_verificador = rut_limpio[-1]
    # Inicializa los valores del algoritmo Módulo 11.
    suma = 0
    multiplicador = 2

    # Recorre el cuerpo desde derecha a izquierda para calcular la suma.
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1

    # Calcula el dígito verificador esperado según Módulo 11.
    resultado = 11 - (suma % 11)
    esperado = "0" if resultado == 11 else "K" if resultado == 10 else str(resultado)
    # Compara el dígito ingresado con el resultado calculado.
    return digito_verificador == esperado


def pedir_rut() -> str:
    """Solicita un RUT válido y verifica su dígito verificador."""
    while True:
        # Solicita el RUT usando el método general de texto obligatorio.
        rut = pedir_texto("RUT: ")
        # Devuelve el RUT cuando supera la validación.
        if verificar_rut(rut):
            return rut
        # Informa que el RUT debe corregirse.
        print("RUT inválido. Revisa el número y el dígito verificador.")


def pedir_tipo_direccion() -> str:
    """Solicita uno de los tipos de dirección permitidos."""
    # Construye la lista de tipos permitidos para mostrarla en pantalla.
    tipos_validos = ", ".join(Direccion.TIPOS_DIRECCION)
    # Repite la solicitud hasta elegir un tipo válido.
    while True:
        # Lee el tipo y lo normaliza a minúsculas.
        tipo = pedir_texto(f"Tipo de dirección ({tipos_validos}): ").lower()
        # Devuelve el tipo si está permitido por Direccion.
        if tipo in Direccion.TIPOS_DIRECCION:
            return tipo
        # Informa los valores aceptados.
        print(f"Tipo inválido. Usa: {tipos_validos}.")


def ingresar_direccion() -> Direccion:
    # Muestra el encabezado del formulario de dirección.
    print("\n--- Datos de la dirección ---")
    # Construye la dirección usando los datos ingresados por consola.
    return Direccion(
        idDireccion=pedir_entero("ID de dirección: "),
        tipoDireccion=pedir_tipo_direccion(),
        calle=pedir_texto("Calle: "),
        numero=pedir_texto("Número: "),
        referencia=pedir_texto("Referencia: "),
    )


def ingresar_socio(direccion: Direccion) -> Socio:
    """Solicita los datos necesarios para registrar un socio."""
    # Muestra el encabezado del formulario del socio.
    print("\n--- Datos del socio ---")
    # Construye el socio y reutiliza la dirección ya registrada.
    return Socio(
        estadoActivo=True,
        rut=pedir_rut(),
        edad=pedir_edad(),
        nombres=pedir_texto("Nombres: "),
        apellidoPaterno=pedir_texto("Apellido paterno: "),
        apellidoMaterno=pedir_texto("Apellido materno: "),
        telefono=pedir_texto("Teléfono: "),
        correoElectronico=pedir_texto("Correo electrónico: "),
        direccion=direccion,
    )


def mostrar_socio(socio: Socio) -> None:
    """Muestra los datos del socio, su dirección y su membresía."""
    # Obtiene la dirección asociada para mostrarla junto al socio.
    direccion = socio.getDireccion()

    # Muestra los datos personales del socio.
        # Muestra la información de su dirección.
    print("\n=== Socio registrado ===")
    print(f"RUT: {socio.getRut()}")
    print(f"Edad: {socio.getEdad()} años")
    print(f"Nombre: {socio.getNombres()} {socio.getApellidoPaterno()} "
        f"{socio.getApellidoMaterno()}")
    print(f"Teléfono: {socio.getTelefono()}")
    print(f"Correo: {socio.getCorreoElectronico()}")
    print(f"Teléfono válido: {'Sí' if socio.validarTelefono() else 'No'}")
    print(f"Correo válido: {'Sí' if socio.validarCorreoElectronico() else 'No'}")
    print("\nDirección:")
    print(f"  ID: {direccion.getIdDireccion()}")
    print(f"  Tipo: {direccion.getTipoDireccion()}")
    print(f"  Calle: {direccion.getCalle()} {direccion.getNumero()}")
    print(f"  Referencia: {direccion.getReferencia()}")

    # Obtiene la primera membresía para mostrar su período.
    membresia = socio.membresias[0]
    # Muestra las fechas y el estado actual de la membresía.
    print("\nMembresía:")
    print(f"  Inicio: {membresia.fechaInicio}")
    print(f"  Término: {membresia.fechaTermino}")
    print(f"  Vigente: {'Sí' if socio.tieneMembresiaVigente() else 'No'}")


def main() -> None:
    # Muestra el título de la aplicación de consola.
    print("=== Registro de Socio - PowerFit ===")
    # Solicita y guarda la dirección del socio.
    direccion = ingresar_direccion()
    # Solicita y guarda los datos personales del socio.
    socio = ingresar_socio(direccion)

    # Obtiene la fecha actual para iniciar la membresía.
    hoy = date.today()
    # Crea una membresía inicial de 30 días.
    membresia = MembresiaMensual(hoy, hoy + timedelta(days=30))
    # Asocia la membresía al socio.
    socio.membresias.append(membresia)

    # Crea una clase de Yoga de ejemplo.
    clase = Yoga(
        nivel="Inicial",
        codigo=1,
        nombre="Yoga de la mañana",
        cupoMaximo=10,
        duracionMinutos=60,
    )
    # Inscribe al socio en la clase creada.
    clase.inscribirSocio(socio)

    # Muestra toda la información registrada.
    mostrar_socio(socio)
    # Muestra el nombre de la clase y sus cupos restantes.
    print(f"\nClase: {clase.nombre}")
    print(f"Cupos disponibles: {clase.calcularCuposDisponibles()}")


if __name__ == "__main__":
    # Ejecuta el flujo de consola solo cuando este archivo se inicia directamente.
    main()