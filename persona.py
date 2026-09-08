# Define la clase llamada Persona que servirá como plantilla para representar a una persona en el sistema.
class Persona:
    # Método constructor que inicializa los atributos de una nueva instancia de la clase Persona.
    def __init__(self, rut: str, nombre: str, apellidoPaterno: str, apellidoMaterno: str):
        # Asigna el parámetro 'rut' de tipo str al atributo de instancia correspondiente.
        self.rut = rut
        # Asigna el parámetro 'nombre' de tipo str al atributo de instancia correspondiente.
        self.nombre = nombre
        # Asigna el parámetro 'apellidoPaterno' de tipo str al atributo de instancia correspondiente.
        self.apellidoPaterno = apellidoPaterno
        # Asigna el parámetro 'apellidoMaterno' de tipo str al atributo de instancia correspondiente.
        self.apellidoMaterno = apellidoMaterno
