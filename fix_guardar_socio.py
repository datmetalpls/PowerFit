import re
with open("src/gui/app_window.py", "r") as f:
    code = f.read()

guardar_socio_old = """    def guardar_socio(self):
        rut = self.input_rut.text().strip()
        nombres = self.input_nombres.text().strip()
        apellidos = self.input_apellidos.text().strip()
        telefono = self.input_telefono.text().strip()
        comuna = self.combo_comunas.currentText()
        tipo_direccion = self.combo_tipo_direccion.currentText()

        if not rut or not nombres or not apellidos:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor completa al menos RUT, Nombres y Apellidos")
            return

        nombre_comuna = comuna.split(" (ID:")[0]


        # Evaluar estado inicial seleccionado"""

guardar_socio_new = """    def guardar_socio(self):
        rut = self.input_rut.text().strip()
        nombres = self.input_nombres.text().strip()
        apellido_pat = self.input_apellido_paterno.text().strip()
        apellido_mat = self.input_apellido_materno.text().strip()
        telefono = self.input_telefono.text().strip()

        if not rut or not nombres or not apellido_pat:
            QMessageBox.warning(self, "Campos Incompletos", "Por favor completa al menos RUT, Nombres y Apellido Paterno")
            return

        # Evaluar estado inicial seleccionado"""
code = code.replace(guardar_socio_old, guardar_socio_new)

with open("src/gui/app_window.py", "w") as f:
    f.write(code)

