with open("src/gui/app_window.py", "r") as f:
    lines = f.readlines()

out = []
skip = False
for line in lines:
    if "tipo_dir_mapeo = tipo_direccion.lower()" in line:
        skip = True
        continue
    
    if skip:
        if line.strip() == ")":
            skip = False
        continue

    out.append(line)

with open("src/gui/app_window.py", "w") as f:
    f.writelines(out)

