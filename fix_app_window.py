import re

with open("src/gui/app_window.py", "r") as f:
    code = f.read()

# 1. Fix Inscription return
# The block is inside hacer_clic_puesto:
#            ya_inscrito = any(s is not None and s.idSocio == socio.idSocio for s in clase.cupos)
#            if ya_inscrito:
#                QMessageBox.warning(self, "Doble Inscripción", f"El socio {socio.nombres} ya está inscrito en esta clase.")
#                return
# Wait, let's see exactly what's there.

def fix_inscription(code_text):
    old_ya_inscrito = 'ya_inscrito = any(s is not None and s.idSocio == socio.idSocio for s in self.clase_seleccionada_actual.cupos)'
    # ensure there's a return if found.
    # Wait, earlier I might not have added the check to the correct place.
    if old_ya_inscrito not in code_text:
        # let's inject it before `exito = self.clase_seleccionada_actual.inscribir_socio(socio, posicion)`
        injection_point = '            try:\n                exito = self.clase_seleccionada_actual.inscribir_socio(socio, posicion)'
        injected = '''            ya_inscrito = any(s is not None and s.idSocio == socio.idSocio for s in self.clase_seleccionada_actual.cupos)
            if ya_inscrito:
                QMessageBox.warning(self, "Doble Inscripción", f"El socio {socio.getNombres()} ya está inscrito en esta clase.")
                return

            try:
                exito = self.clase_seleccionada_actual.inscribir_socio(socio, posicion)'''
        code_text = code_text.replace(injection_point, injected)
    return code_text

# 2. Fix Ventas double discount
def fix_ventas(code_text):
    # Remove these lines:
    to_remove = '''        # Descontar stock y actualizar SQLite
        obj_suplemento.descontarStock(cant)
        self.suplemento_dao.guardar(obj_suplemento)

        # Refrescar vista del combo y la tabla de inventario en tiempo real
        self.actualizar_inventario_y_combo()'''
    
    code_text = code_text.replace(to_remove, '')
    
    # And move `self.actualizar_inventario_y_combo()` to after `self.cargar_historial_ventas_bd()`
    injection_point2 = '''        self.cargar_historial_ventas_bd()

        QMessageBox.information('''
    injected2 = '''        self.cargar_historial_ventas_bd()

        # Refrescar vista del combo guardando el indice
        idx_previo = self.combo_producto.currentIndex()
        self.actualizar_inventario_y_combo()
        if idx_previo >= 0 and idx_previo < self.combo_producto.count():
            self.combo_producto.setCurrentIndex(idx_previo)

        if not exito:
            QMessageBox.warning(self, "Error", "No se pudo agregar el detalle de venta (Posible falta de stock local).")
            return

        QMessageBox.information('''
    
    code_text = code_text.replace(injection_point2, injected2)
    return code_text

code = fix_inscription(code)
code = fix_ventas(code)

with open("src/gui/app_window.py", "w") as f:
    f.write(code)

