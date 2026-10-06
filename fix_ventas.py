with open("src/dao/conexion.py", "r") as f:
    conn_code = f.read()

alter_ventas = """
            # Auto-migrar ventas
            cursor.execute("PRAGMA table_info(ventas);")
            columnas_existentes_ventas = [col['name'] for col in cursor.fetchall()]
            if 'tasa_cambio_usd' not in columnas_existentes_ventas:
                cursor.execute("ALTER TABLE ventas ADD COLUMN tasa_cambio_usd REAL DEFAULT 0.0;")
"""
conn_code = conn_code.replace('            # 7. Tabla Detalle Ventas', alter_ventas + '            # 7. Tabla Detalle Ventas')
with open("src/dao/conexion.py", "w") as f:
    f.write(conn_code)

with open("src/dao/venta_dao.py", "r") as f:
    venta_code = f.read()

# Point 3 and 4 fixes
old_obtener = """
            cursor.execute(\"\"\"
                SELECT v.id_venta, v.numero, v.fecha, v.total_clp,
                       dv.id_suplemento, dv.cantidad, dv.precio_unitario_clp,
                       s.nombre AS nombre_suplemento
                FROM ventas v"""
new_obtener = """
            cursor.execute(\"\"\"
                SELECT v.id_venta, v.numero, v.fecha, v.total_clp, v.tasa_cambio_usd,
                       dv.id_suplemento, dv.cantidad, dv.precio_unitario_clp,
                       s.nombre AS nombre_suplemento
                FROM ventas v"""
venta_code = venta_code.replace(old_obtener, new_obtener)

old_append = """
                ventas.append({
                    "id_venta": row['id_venta'],
                    "numero": row['numero'],
                    "fecha": row['fecha'],
                    "total_clp": row['total_clp'],
                    "nombre_producto": row['nombre_suplemento'] or "Suplemento",
                    "cantidad": row['cantidad'] or 0,
                    "precio_unitario": row['precio_unitario_clp'] or 0.0
                })"""
new_append = """
                ventas.append({
                    "id_venta": row['id_venta'],
                    "numero": row['numero'],
                    "fecha": row['fecha'],
                    "total_clp": row['total_clp'],
                    "tasa_cambio_usd": row['tasa_cambio_usd'] or 0.0,
                    "nombre_producto": row['nombre_suplemento'] or "Suplemento",
                    "cantidad": row['cantidad'] or 0,
                    "precio_unitario": row['precio_unitario_clp'] or 0.0
                })"""
venta_code = venta_code.replace(old_append, new_append)

old_guardar = """
        fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(\"\"\"
                INSERT INTO ventas (numero, fecha, total_clp)
                VALUES (?, ?, ?);
            \"\"\", (entidad.numero, fecha_str, entidad.totalCLP))
            id_venta = cursor.lastrowid

            for det in entidad.detalles:
                id_sup = int(det.suplemento.codigo) if det.suplemento.codigo.isdigit() else 1
                cursor.execute(\"\"\"
                    INSERT INTO detalles_ventas (id_venta, id_suplemento, cantidad, precio_unitario_clp)
                    VALUES (?, ?, ?, ?);
                \"\"\", (id_venta, id_sup, det.cantidad, det.precioUnitarioCLP))

            conn.commit()
"""
new_guardar = """
        fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Extract tasa_cambio_usd (which is stored in suplemento for today)
        tasa_usd = 0.0
        if entidad.detalles:
            tasa_usd = entidad.detalles[0].suplemento.precio_clp / entidad.detalles[0].suplemento.precio_usd if entidad.detalles[0].suplemento.precio_usd > 0 else 0.0

        with ConexionDB.obt_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(\"\"\"
                INSERT INTO ventas (numero, fecha, total_clp, tasa_cambio_usd)
                VALUES (?, ?, ?, ?);
            \"\"\", (entidad.numero, fecha_str, entidad.totalCLP, tasa_usd))
            id_venta = cursor.lastrowid

            for det in entidad.detalles:
                id_sup = int(det.suplemento.codigo) if det.suplemento.codigo.isdigit() else 1
                cursor.execute(\"\"\"
                    INSERT INTO detalles_ventas (id_venta, id_suplemento, cantidad, precio_unitario_clp)
                    VALUES (?, ?, ?, ?);
                \"\"\", (id_venta, id_sup, det.cantidad, det.precioUnitarioCLP))
                
                # Descontar stock (Point 4)
                cursor.execute(\"\"\"
                    UPDATE suplementos SET stock = stock - ? WHERE id_suplemento = ?;
                \"\"\", (det.cantidad, id_sup))

            conn.commit()
"""
venta_code = venta_code.replace(old_guardar, new_guardar)

with open("src/dao/venta_dao.py", "w") as f:
    f.write(venta_code)

with open("src/gui/app_window.py", "r") as f:
    gui = f.read()

gui = gui.replace('self.tabla_ventas.setColumnCount(4)\n        self.tabla_ventas.setHorizontalHeaderLabels(["Producto", "Cant.", "V. Dólar", "Total Estimado"])', 'self.tabla_ventas.setColumnCount(5)\n        self.tabla_ventas.setHorizontalHeaderLabels(["Producto", "Cant.", "P. USD", "Tasa USD", "Total CLP"])')
gui = gui.replace('self.tabla_historial.setColumnCount(4)\n        self.tabla_historial.setHorizontalHeaderLabels(["Fecha", "N° Boleta", "Artículos", "Total $"])', 'self.tabla_historial.setColumnCount(5)\n        self.tabla_historial.setHorizontalHeaderLabels(["Fecha", "N° Boleta", "Artículos", "Tasa USD", "Total CLP"])')

old_table_pop = """
            self.tabla_historial.setItem(r, 0, QTableWidgetItem(str(v["fecha"])))
            self.tabla_historial.setItem(r, 1, QTableWidgetItem(str(v["numero"])))
            self.tabla_historial.setItem(r, 2, QTableWidgetItem(f"{v['cantidad']}x {v['nombre_producto']}"))
            self.tabla_historial.setItem(r, 3, QTableWidgetItem(f"${v['total_clp']:,.0f}"))"""
new_table_pop = """
            self.tabla_historial.setItem(r, 0, QTableWidgetItem(str(v["fecha"])))
            self.tabla_historial.setItem(r, 1, QTableWidgetItem(str(v["numero"])))
            self.tabla_historial.setItem(r, 2, QTableWidgetItem(f"{v['cantidad']}x {v['nombre_producto']}"))
            self.tabla_historial.setItem(r, 3, QTableWidgetItem(f"${v['tasa_cambio_usd']:,.0f}"))
            self.tabla_historial.setItem(r, 4, QTableWidgetItem(f"${v['total_clp']:,.0f}"))"""
gui = gui.replace(old_table_pop, new_table_pop)

with open("src/gui/app_window.py", "w") as f:
    f.write(gui)
