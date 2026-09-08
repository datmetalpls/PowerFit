# Clase Persona: Plantilla base para representar a las personas dentro del sistema PowerFit.
class Persona:
    # Atributos de clase según la especificación del diagrama UML
    rut: str
    nombres: str
    apellidoPaterno: str
    apellidoMaterno: str
    telefono: str
    correoElectronico: str

    # Método constructor que inicializa los atributos de la instancia Persona
    def __init__(
        self,
        rut: str,
        nombres: str,
        apellidoPaterno: str,
        apellidoMaterno: str,
        telefono: str,
        correoElectronico: str,
    ):
        # Asignación del RUT de la persona
        self.rut = rut
        # Asignación de los nombres de la persona
        self.nombres = nombres
        # Asignación del apellido paterno
        self.apellidoPaterno = apellidoPaterno
        # Asignación del apellido materno
        self.apellidoMaterno = apellidoMaterno
        # Asignación del teléfono de contacto
        self.telefono = telefono
        # Asignación del correo electrónico de contacto
        self.correoElectronico = correoElectronico

    # Método para validar el formato y la validez del RUT de la persona según el diagrama UML
    def validarRut(self) -> bool:
        """
        Valida que el RUT de la persona cumpla con un formato válido.
        Retorna True si es válido, False en caso contrario.
        """
        pass

    # Método para validar el formato del número telefónico de contacto según el diagrama UML
    def validarTelefono(self) -> bool:
        """
        Valida que el número telefónico de la persona sea válido.
        Retorna True si es válido, False en caso contrario.
        """
        pass

    # Método para validar el formato de la dirección de correo electrónico según el diagrama UML
    def validarCorreoElectronico(self) -> bool:
        """
        Valida que la dirección de correo electrónico de la persona tenga un formato correcto.
        Retorna True si es válido, False en caso contrario.
        """
        pass


