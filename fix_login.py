with open("src/gui/app_window.py", "r") as f:
    code = f.read()

old_login = """
    def iniciar_sesion(self):
        usr = self.input_login_usuario.text().strip()
        pwd = self.input_login_password.text().strip()

        if not usr or not pwd:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor ingresa usuario y contraseña.")
            return

        if usr in self.usuarios_sistema and self.usuarios_sistema[usr].autenticar(pwd):
            self.usuario_actual = self.usuarios_sistema[usr]"""

new_login = """
    def iniciar_sesion(self):
        if getattr(self, 'intentos_login', 0) >= 3:
            QMessageBox.critical(self, "Sistema Bloqueado", "Superó los 3 intentos. Acceso bloqueado.")
            return

        usr = self.input_login_usuario.text().strip()
        pwd = self.input_login_password.text().strip()

        if not usr or not pwd:
            QMessageBox.warning(self, "Campos Vacíos", "Por favor ingresa usuario y contraseña.")
            return

        if usr in self.usuarios_sistema and self.usuarios_sistema[usr].autenticar(pwd):
            self.intentos_login = 0  # Reset
            self.usuario_actual = self.usuarios_sistema[usr]"""
code = code.replace(old_login, new_login)

old_fail = """        else:
            QMessageBox.warning(self, "Error de Autenticación", "Usuario o contraseña incorrectos.")"""
new_fail = """        else:
            self.intentos_login = getattr(self, 'intentos_login', 0) + 1
            quedan = 3 - self.intentos_login
            if quedan > 0:
                QMessageBox.warning(self, "Error de Autenticación", f"Usuario o contraseña incorrectos.\\nLe quedan {quedan} intentos.")
            else:
                QMessageBox.critical(self, "Cuenta Bloqueada", "Ha superado los 3 intentos fallidos. El acceso ha sido bloqueado.")
                self.btn_login.setEnabled(False)"""
code = code.replace(old_fail, new_fail)

with open("src/gui/app_window.py", "w") as f:
    f.write(code)
