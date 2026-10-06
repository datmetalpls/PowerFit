import re

with open("src/gui/app_window.py", "r") as f:
    code = f.read()

# 1. Remove Direccion and Comuna imports
code = re.sub(r'from src\.models\.direccion import Direccion\n?', '', code)
code = re.sub(r'from src\.models\.comuna import Comuna\n?', '', code)

# 2. Fix the login attempts (Point 7)
login_init = """    def __init__(self):
        super().__init__()
        self.intentos_login = 0"""
code = code.replace("    def __init__(self):\n        super().__init__()", login_init, 1)

login_logic = """        if hasattr(self, 'intentos_login') and self.intentos_login >= 3:
            QMessageBox.critical(self, "Cuenta Bloqueada", "Demasiados intentos fallidos. Sistema bloqueado.")
            return

        usuario = self.input_usr.text()
        password = self.input_pwd.text()

        trabajador_autenticado = self.trabajador_dao.autenticar(usuario, password)

        if trabajador_autenticado:
            self.intentos_login = 0"""
code = re.sub(r'        usuario = self.input_usr.text\(\)\s+password = self.input_pwd.text\(\)\s+trabajador_autenticado = self.trabajador_dao.autenticar\(usuario, password\)\s+if trabajador_autenticado:', login_logic, code)

fail_logic = """        else:
            self.intentos_login = getattr(self, 'intentos_login', 0) + 1
            quedan = 3 - self.intentos_login
            if quedan > 0:
                QMessageBox.warning(self, "Error de Acceso", f"Credenciales incorrectas.\\nLe quedan {quedan} intentos.")
            else:
                QMessageBox.critical(self, "Cuenta Bloqueada", "Ha superado los 3 intentos fallidos. El acceso ha sido bloqueado.")
                self.btn_login.setEnabled(False)"""
code = code.replace("""        else:\n            QMessageBox.warning(self, "Error de Acceso", "Usuario o contraseña incorrectos.")""", fail_logic)


# 3. Socios form: remove comuna and direccion, split apellidos
code = code.replace('self.input_apellidos = QLineEdit()', 'self.input_apellido_paterno = QLineEdit()\n        self.input_apellido_materno = QLineEdit()')
code = code.replace('form_socios.addRow("Apellidos: ", self.input_apellidos)', 'form_socios.addRow("Apellido Paterno: ", self.input_apellido_paterno)\n        form_socios.addRow("Apellido Materno: ", self.input_apellido_materno)')

# Remove Comuna and Vivienda
code = re.sub(r'        self\.combo_comuna = QComboBox\(\)\n.*?form_socios\.addRow\("Tipo Vivienda: ", self\.combo_tipo_direccion\)\n', '', code, flags=re.DOTALL)

# Modify registro socio (lines ~464)
reg_socio_old = """        apellidos = self.input_apellidos.text().strip()
        telefono = self.input_telefono.text().strip()
        correo = self.input_correo.text().strip()
        tipo_direccion = self.combo_tipo_direccion.currentText()
        comuna_seleccionada = self.combo_comuna.currentText()

        if not rut or not nombres or not apellidos:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor, complete al menos RUT, Nombres y Apellidos.")
            return

        # Mapear el tipo de direccion a lo esperado por la validacion
        tipo_dir_mapeo = tipo_direccion.lower()
        if "departamento" in tipo_dir_mapeo:
            tipo_dir_mapeo = "dpto"

        obj_direccion = Direccion(
            idDireccion=0,
            tipoDireccion=tipo_dir_mapeo,
            calle="Av. Siempre Viva",
            numero="742",
            referencia="Cerca del parque",
            comuna=Comuna(0, comuna_seleccionada)
        )"""

reg_socio_new = """        apellido_pat = self.input_apellido_paterno.text().strip()
        apellido_mat = self.input_apellido_materno.text().strip()
        telefono = self.input_telefono.text().strip()
        correo = self.input_correo.text().strip()

        if not rut or not nombres or not apellido_pat:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor, complete al menos RUT, Nombres y Apellido Paterno.")
            return"""
code = code.replace(reg_socio_old, reg_socio_new)

# Modify the Socio object creation
socio_creation_old = """                apellidoPaterno=apellidos,
                apellidoMaterno="",
                telefono=telefono,
                correoElectronico=correo,
                fechaVencimientoMembresia=None,
                estadoActivo=True
            )
            # Vincular direccion
            nuevo_socio.direccion = obj_direccion"""

socio_creation_new = """                apellidoPaterno=apellido_pat,
                apellidoMaterno=apellido_mat,
                telefono=telefono,
                correoElectronico=correo,
                fechaVencimientoMembresia=None,
                estadoActivo=True
            )"""
code = code.replace(socio_creation_old, socio_creation_new)

code = code.replace('f"¡Socio {nombres} {apellidos} registrado exitosamente y guardado en SQLite!\\n"', 'f"¡Socio {nombres} {apellido_pat} registrado exitosamente y guardado en SQLite!\\n"')
code = code.replace('self.input_apellidos.clear()', 'self.input_apellido_paterno.clear()\n            self.input_apellido_materno.clear()')

# 4. Socios Table headers and population
code = code.replace('["RUT", "Nombre Completo", "Teléfono", "Comuna", "Vivienda", "Membresía"]', '["RUT", "Nombres", "Ap. Paterno", "Ap. Materno", "Teléfono", "Membresía"]')

table_pop_old = """            self.tabla_socios.setItem(row, 1, QTableWidgetItem(f"{socio.nombres} {socio.apellidoPaterno}"))
            self.tabla_socios.setItem(row, 2, QTableWidgetItem(socio.telefono))

            # Manejo defensivo por si direccion/comuna no estan cargados en la BD aun
            comuna_nombre = socio.direccion.comuna.nombre if getattr(socio, 'direccion', None) and getattr(socio.direccion, 'comuna', None) else "N/A"
            vivienda_tipo = socio.direccion.tipoDireccion if getattr(socio, 'direccion', None) else "N/A"

            self.tabla_socios.setItem(row, 3, QTableWidgetItem(comuna_nombre))
            self.tabla_socios.setItem(row, 4, QTableWidgetItem(vivienda_tipo))"""

table_pop_new = """            self.tabla_socios.setItem(row, 1, QTableWidgetItem(socio.nombres))
            self.tabla_socios.setItem(row, 2, QTableWidgetItem(socio.apellidoPaterno))
            self.tabla_socios.setItem(row, 3, QTableWidgetItem(socio.apellidoMaterno))
            self.tabla_socios.setItem(row, 4, QTableWidgetItem(socio.telefono))"""
code = code.replace(table_pop_old, table_pop_new)

# 5. Personal form split apellidos
code = code.replace('self.input_trab_apellidos = QLineEdit()', 'self.input_trab_apellido_pat = QLineEdit()\n        self.input_trab_apellido_mat = QLineEdit()')
code = code.replace('form_personal.addRow("Apellidos: ", self.input_trab_apellidos)', 'form_personal.addRow("Apellido Paterno: ", self.input_trab_apellido_pat)\n        form_personal.addRow("Apellido Materno: ", self.input_trab_apellido_mat)')
code = code.replace('apellidos = self.input_trab_apellidos.text().strip()', 'apellido_pat = self.input_trab_apellido_pat.text().strip()\n        apellido_mat = self.input_trab_apellido_mat.text().strip()')
code = code.replace('apellidoPaterno=apellidos', 'apellidoPaterno=apellido_pat, apellidoMaterno=apellido_mat')
code = code.replace('self.input_trab_apellidos.clear()', 'self.input_trab_apellido_pat.clear()\n                self.input_trab_apellido_mat.clear()')


# 6. Prevent multiple seats logic in clase (Point 6)
hacer_clic_old = """            # Intentar inscribirlo via POO
            exito = clase.inscribir_socio(socio, posicion)
            if exito:
                # Guardar inscripción permanente en SQLite
                cod_str = str(getattr(clase, 'codigo', '0'))
                id_clase_num = int(''.join(filter(str.isdigit, cod_str)) or '0')
                self.inscripcion_dao.inscribir_socio(socio.idSocio, id_clase_num)"""

hacer_clic_new = """            # Validar que el socio no esté ya en la clase (Point 6)
            ya_inscrito = any(s is not None and s.idSocio == socio.idSocio for s in clase.cupos)
            if ya_inscrito:
                QMessageBox.warning(self, "Doble Inscripción", f"El socio {socio.nombres} ya está inscrito en esta clase.")
                return

            # Intentar inscribirlo via POO
            exito = clase.inscribir_socio(socio, posicion)
            if exito:
                # Guardar inscripción permanente en SQLite
                cod_str = str(getattr(clase, 'codigo', '0'))
                id_clase_num = int(''.join(filter(str.isdigit, cod_str)) or '0')
                self.inscripcion_dao.inscribir_socio(socio.idSocio, id_clase_num)"""
code = code.replace(hacer_clic_old, hacer_clic_new)

# Remove unused update_comunas function
code = re.sub(r'    def cargar_comunas_ine\(self\):.*?            self\.combo_comuna\.addItems\(comunas_ordenadas\)', '', code, flags=re.DOTALL)


with open("src/gui/app_window.py", "w") as f:
    f.write(code)

