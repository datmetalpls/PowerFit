# Plan de Correcciones PowerFit - Fase 2

## 1. Validación de Clases Dirigidas (Doble Asiento)
- **Problema detectado:** Aunque agregamos el código, la validación se hace tarde o tiene un pequeño bug con la referencia al socio.
- **Propuesta:** Asegurar que el chequeo `any(s is not None and s.idSocio == socio.idSocio ...)` se ejecute de forma robusta e interrumpa el flujo con un `QMessageBox.warning` antes de intentar agregar.

## 2. Ventas (Combobox, Mensaje y Descuentos Múltiples)
- **Problema detectado:** El código estaba descontando el stock 3 veces: en la GUI, en el modelo `Venta.agregarDetalle` y luego a nivel SQL en `VentaDAO`. Esto provocaba que `agregarDetalle` fallara por falta de stock ficticia, dejando el detalle vacío. Además, el combobox perdía la selección porque la tabla se redibujaba antes del final del flujo.
- **Propuesta:** 
  1. Dejar que solo `VentaDAO` descuente el stock físicamente en la BD durante el guardado de la venta.
  2. Mover el refresco del inventario (`actualizar_inventario_y_combo()`) al final del proceso de venta.
  3. Guardar el `currentIndex` del combobox y restaurarlo tras el refresco para que no salte de nuevo al primer elemento.

## 3. Flush de Base de Datos
- **Problema detectado:** Posibles datos sucios o esquemas mezclados durante las pruebas previas.
- **Propuesta:** Se borrará físicamente el archivo `database/powerfit.db` antes de correr la aplicación. Al iniciar, SQLite regenerará la tabla limpia con todas las nuevas columnas de la Fase 1.

> **[!] ACCIÓN REQUERIDA:** Presiona "Proceed" o confírmame por chat para aplicar estas mejoras finales y hacer el flush a la BD.
