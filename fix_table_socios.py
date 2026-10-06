with open("src/gui/app_window.py", "r") as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if "self.tabla_socios.setItem(row, 1, QTableWidgetItem(f\"{socio.nombres} {socio.apellidoPaterno}\"))" in line:
        out.append("            self.tabla_socios.setItem(row, 1, QTableWidgetItem(socio.nombres))\n")
        out.append("            self.tabla_socios.setItem(row, 2, QTableWidgetItem(socio.apellidoPaterno))\n")
        out.append("            self.tabla_socios.setItem(row, 3, QTableWidgetItem(socio.apellidoMaterno))\n")
        out.append("            self.tabla_socios.setItem(row, 4, QTableWidgetItem(socio.telefono))\n")
        skip = True
        continue
    
    if skip and "lbl_estado =" in line:
        skip = False

    if not skip:
        out.append(line)

with open("src/gui/app_window.py", "w") as f:
    f.writelines(out)
