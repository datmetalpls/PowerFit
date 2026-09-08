# Define la clase llamada Persona que servirá como plantilla para representar a una persona en el sistema.
class Persona:
    # Atributos de la clase según el diagrama UML (ProyectGym)
    rut: str
    nombres: str
    apellidoPaterno: str
    apellidoMaterno: str
    telefono: str
    correoElectronico: str

    # Método constructor que inicializa los atributos de una nueva instancia de la clase Persona.
    def __init__(
        self,
        rut: str,
        nombres: str = "",
        apellidoPaterno: str = "",
        apellidoMaterno: str = "",
        telefono: str = "",
        correoElectronico: str = "",
        nombre: str = None,
    ):
        # Asigna el parámetro 'rut' de tipo str al atributo de instancia correspondiente.
        self.rut = rut
        # Asigna el parámetro 'nombres' (o 'nombre' por compatibilidad) de tipo str al atributo de instancia correspondiente.
        self.nombres = nombre if nombre is not None else nombres
        # Asigna el parámetro 'apellidoPaterno' de tipo str al atributo de instancia correspondiente.
        self.apellidoPaterno = apellidoPaterno
        # Asigna el parámetro 'apellidoMaterno' de tipo str al atributo de instancia correspondiente.
        self.apellidoMaterno = apellidoMaterno
        # Asigna el parámetro 'telefono' de tipo str al atributo de instancia correspondiente.
        self.telefono = telefono
        # Asigna el parámetro 'correoElectronico' de tipo str al atributo de instancia correspondiente.
        self.correoElectronico = correoElectronico

    @property
    def nombre(self) -> str:
        """Alias para mantener compatibilidad si se consulta 'nombre' en singular."""
        return self.nombres

    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.nombres = valor
