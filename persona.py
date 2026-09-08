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
        # Encapsulamiento de atributos (convención '_' para variables protegidas/privadas)
        # Asignación del RUT de la persona (identificador único e inmutable)
        self._rut = rut
        # Asignación de los nombres de la persona (identidad legal inmutable)
        self._nombres = nombres
        # Asignación del apellido paterno (identidad legal inmutable)
        self._apellidoPaterno = apellidoPaterno
        # Asignación del apellido materno (identidad legal inmutable)
        self._apellidoMaterno = apellidoMaterno
        # Asignación del teléfono de contacto (dato dinámico modificable)
        self._telefono = telefono
        # Asignación del correo electrónico de contacto (dato dinámico modificable)
        self._correoElectronico = correoElectronico

    # =========================================================================
    # MÉTODOS GETTER (Lectura de atributos)
    # Permiten acceder al valor de los atributos encapsulados de forma controlada.
    # =========================================================================

    # --- 1. RUT ---
    # Función: Obtener y retornar el RUT de la persona.
    # Razón: Es indispensable para identificar a la persona en consultas, búsquedas y reportes.
    #        No tiene método 'set' porque el RUT es la clave primaria natural e inmutable;
    #        modificarlo comprometería la integridad de membresías, asistencias y contratos.
    def getRut(self) -> str:
        """Retorna el RUT de la persona (identificador inmutable)."""
        return self._rut

    # --- 2. NOMBRES ---
    # Función: Obtener y retornar los nombres de la persona.
    # Razón: Permite mostrar el nombre del socio o trabajador en pantallas, credenciales y recibos.
    #        No tiene método 'set' para proteger la identidad legal registrada del titular
    #        y prevenir suplantaciones o transferencias no autorizadas de membresías.
    def getNombres(self) -> str:
        """Retorna los nombres de la persona (identidad inmutable)."""
        return self._nombres

    # --- 3. APELLIDO PATERNO ---
    # Función: Obtener y retornar el apellido paterno de la persona.
    # Razón: Individualiza legal y formalmente a la persona en el sistema PowerFit.
    #        No tiene método 'set' por formar parte de la identidad civil legal inmutable.
    def getApellidoPaterno(self) -> str:
        """Retorna el apellido paterno de la persona (identidad inmutable)."""
        return self._apellidoPaterno

    # --- 4. APELLIDO MATERNO ---
    # Función: Obtener y retornar el apellido materno de la persona.
    # Razón: Completa la filiación civil de la persona para registros oficiales y contratos.
    #        No tiene método 'set' por formar parte de la identidad civil legal inmutable.
    def getApellidoMaterno(self) -> str:
        """Retorna el apellido materno de la persona (identidad inmutable)."""
        return self._apellidoMaterno

    # --- 5. TELÉFONO ---
    # Función: Obtener y retornar el número de teléfono de contacto.
    # Razón: Permite consultar la vía de contacto telefónico para coordinaciones y recordatorios.
    def getTelefono(self) -> str:
        """Retorna el número de teléfono de contacto de la persona."""
        return self._telefono

    # --- 6. CORREO ELECTRÓNICO ---
    # Función: Obtener y retornar la dirección de correo electrónico de contacto.
    # Razón: Permite consultar el correo para el envío de notificaciones y comprobantes de pago.
    def getCorreoElectronico(self) -> str:
        """Retorna el correo electrónico de contacto de la persona."""
        return self._correoElectronico

    # =========================================================================
    # MÉTODOS SETTER (Modificación de atributos)
    # Permiten actualizar el valor de aquellos atributos que son dinámicos/mutables.
    # Nota de diseño: Los datos de identidad (rut, nombres, apellidos) NO poseen setter
    # para garantizar la inmutabilidad y la seguridad jurídica del sistema.
    # =========================================================================

    # --- SET TELÉFONO ---
    # Función: Modificar y actualizar el número telefónico de contacto.
    # Razón: El teléfono es un dato de contacto dinámico; los socios y trabajadores pueden
    #        cambiar de número, por lo que el sistema debe permitir su actualización.
    def setTelefono(self, telefono: str) -> None:
        """Modifica el número de teléfono de contacto de la persona."""
        self._telefono = telefono

    # --- SET CORREO ELECTRÓNICO ---
    # Función: Modificar y actualizar la dirección de correo electrónico.
    # Razón: El correo es un canal dinámico de comunicación digital; los usuarios pueden
    #        cambiar su dirección y el sistema debe mantenerlo al día para avisos y cobros.
    def setCorreoElectronico(self, correoElectronico: str) -> None:
        """Modifica el correo electrónico de contacto de la persona."""
        self._correoElectronico = correoElectronico


    # Método para validar el formato y la validez del RUT de la persona según el diagrama UML
    def validarRut(self) -> bool:
        """
        Valida que el RUT de la persona cumpla con el algoritmo de Módulo 11.
        Retorna True si el RUT y su dígito verificador son válidos, False en caso contrario.
        """
        if not self._rut or not isinstance(self._rut, str):
            return False

        # Limpiar el RUT de puntos, guiones y espacios, y convertir a mayúsculas
        rut_limpio = self._rut.replace(".", "").replace("-", "").replace(" ", "").upper()

        # Debe contener al menos el cuerpo (mínimo 1 dígito) y el dígito verificador
        if len(rut_limpio) < 2:
            return False

        cuerpo = rut_limpio[:-1]
        dv_ingresado = rut_limpio[-1]

        # El cuerpo del RUT debe ser puramente numérico
        if not cuerpo.isdigit():
            return False

        # Algoritmo de Módulo 11
        suma = 0
        multiplicador = 2

        for digito in reversed(cuerpo):
            suma += int(digito) * multiplicador
            multiplicador = 2 if multiplicador == 7 else multiplicador + 1

        resto = suma % 11
        resultado = 11 - resto

        if resultado == 11:
            dv_esperado = "0"
        elif resultado == 10:
            dv_esperado = "K"
        else:
            dv_esperado = str(resultado)

        return dv_ingresado == dv_esperado

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


