import re

with open("src/dao/conexion.py", "r") as f:
    conn_code = f.read()

# Add new columns via ALTER TABLE for clases
alter_clases = """
            # Auto-migrar columnas si la tabla clases ya existia
            cursor.execute("PRAGMA table_info(clases);")
            columnas_existentes_clases = [col['name'] for col in cursor.fetchall()]
            if 'tipo_disciplina' not in columnas_existentes_clases:
                cursor.execute("ALTER TABLE clases ADD COLUMN tipo_disciplina TEXT DEFAULT '';")
            if 'recurso_fisico' not in columnas_existentes_clases:
                cursor.execute("ALTER TABLE clases ADD COLUMN recurso_fisico INTEGER DEFAULT 0;")
"""

conn_code = conn_code.replace('            # 4. Tabla Inscripciones', alter_clases + '            # 4. Tabla Inscripciones')
with open("src/dao/conexion.py", "w") as f:
    f.write(conn_code)


with open("src/dao/clase_dao.py", "r") as f:
    clase_code = f.read()

map_old = """
        if "spinning" in nombre_lower:
            clase = Spinning(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor)
        elif "yoga" in nombre_lower:
            clase = Yoga(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor)
        else:
            clase = Crossfit(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor)"""

map_new = """
        tipo_disciplina = row['tipo_disciplina'] or ''
        recurso = row['recurso_fisico'] or cupo

        if tipo_disciplina.lower() == "spinning":
            clase = Spinning(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor, bicicletas=recurso)
        elif tipo_disciplina.lower() == "yoga":
            clase = Yoga(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor, colchonetas=recurso)
        elif tipo_disciplina.lower() == "crossfit":
            clase = Crossfit(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor, estacionesTrabajo=recurso)
        else:
            # Fallback legacy
            if "spinning" in nombre_lower:
                clase = Spinning(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor)
            elif "yoga" in nombre_lower:
                clase = Yoga(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor)
            else:
                clase = Crossfit(codigo=codigo_str, nombre=nombre, cupoMaximo=cupo, instructor=instructor)"""
clase_code = clase_code.replace(map_old, map_new)

guardar_old = """
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_clase FROM clases WHERE id_clase = ?;", (id_clase_num,))
            existe = cursor.fetchone()

            if existe and id_clase_num > 0: 
                cursor.execute(\"\"\"
                    UPDATE clases
                    SET nombre = ?, horario = ?, cupo_maximo = ?, id_instructor = ?
                    WHERE id_clase = ?;
                \"\"\", (entidad.nombre, horario_str, entidad.cupoMaximo, id_instructor, id_clase_num))
            else: 
                cursor.execute(\"\"\"
                    INSERT INTO clases (nombre, horario, cupo_maximo, id_instructor)
                    VALUES (?, ?, ?, ?);
                \"\"\", (entidad.nombre, horario_str, entidad.cupoMaximo, id_instructor))
"""

guardar_new = """
        tipo_disciplina = ""
        recurso_fisico = entidad.cupoMaximo
        if isinstance(entidad, Spinning):
            tipo_disciplina = "Spinning"
            recurso_fisico = entidad.bicicletas
        elif isinstance(entidad, Yoga):
            tipo_disciplina = "Yoga"
            recurso_fisico = entidad.colchonetas
        elif isinstance(entidad, Crossfit):
            tipo_disciplina = "Crossfit"
            recurso_fisico = entidad.estacionesTrabajo

        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id_clase FROM clases WHERE id_clase = ?;", (id_clase_num,))
            existe = cursor.fetchone()

            if existe and id_clase_num > 0: 
                cursor.execute(\"\"\"
                    UPDATE clases
                    SET nombre = ?, horario = ?, cupo_maximo = ?, id_instructor = ?, tipo_disciplina = ?, recurso_fisico = ?
                    WHERE id_clase = ?;
                \"\"\", (entidad.nombre, horario_str, entidad.cupoMaximo, id_instructor, tipo_disciplina, recurso_fisico, id_clase_num))
            else: 
                cursor.execute(\"\"\"
                    INSERT INTO clases (nombre, horario, cupo_maximo, id_instructor, tipo_disciplina, recurso_fisico)
                    VALUES (?, ?, ?, ?, ?, ?);
                \"\"\", (entidad.nombre, horario_str, entidad.cupoMaximo, id_instructor, tipo_disciplina, recurso_fisico))
"""
clase_code = clase_code.replace(guardar_old, guardar_new)

with open("src/dao/clase_dao.py", "w") as f:
    f.write(clase_code)

