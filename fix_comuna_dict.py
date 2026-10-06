import re
with open("src/gui/app_window.py", "r") as f:
    code = f.read()

# Remove the loop and related combobox
regex = re.compile(r'        comunas_dict = .*?        layout_izquierdo\.addWidget\(box_registro_socio\)', re.DOTALL)
code = regex.sub('        layout_izquierdo.addWidget(box_registro_socio)', code)

with open("src/gui/app_window.py", "w") as f:
    f.write(code)
