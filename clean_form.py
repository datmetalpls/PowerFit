with open("src/gui/app_window.py", "r") as f:
    lines = f.readlines()

out = []
for line in lines:
    if "comunas_dict" in line: continue
    if "self.combo_tipo_direccion" in line: continue
    if 'addItems(["Casa", "Departamento", "Block", "Otro"])' in line: continue
    if "self.input_calle" in line: continue
    if "self.input_numero" in line: continue
    if "self.input_referencia" in line: continue
    if "self.combo_comunas" in line: continue
    out.append(line)

with open("src/gui/app_window.py", "w") as f:
    f.writelines(out)
