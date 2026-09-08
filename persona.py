class Persona:
    rut: str
    nombres: str
    apellidoPaterno: str
    apellidoMaterno: str
    telefono: str
    correoElectronico: str

    def __init__(
        self,
        rut: str,
        nombres: str,
        apellidoPaterno: str,
        apellidoMaterno: str,
        telefono: str,
        correoElectronico: str,
    ):
        self.rut = rut
        self.nombres = nombres
        self.apellidoPaterno = apellidoPaterno
        self.apellidoMaterno = apellidoMaterno
        self.telefono = telefono
        self.correoElectronico = correoElectronico

