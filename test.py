from persona import Persona

def probar_validar_rut():
    casos_de_prueba = [
        # (RUT, Resultado Esperado, Descripción)
        ("12.345.678-5", True, "RUT válido con formato con puntos y guión"),
        ("123456785", True, "RUT válido sin puntos ni guión"),
        ("14.805.293-K", True, "RUT válido con DV 'K' mayúscula"),
        ("14.805.293-k", True, "RUT válido con DV 'k' minúscula"),
        ("11.111.111-1", True, "RUT válido repetitivo"),
        ("12.345.678-9", False, "RUT con dígito verificador incorrecto"),
        ("12.345.67A-5", False, "RUT con letras en el cuerpo"),
        ("1", False, "RUT demasiado corto"),
        ("", False, "RUT vacío"),
        ("18.045.022-K", True, "RUT válido con DV 'K'"),
    ]

    print("=" * 70)
    print(" 🧪 PRUEBAS UNITARIAS: Método validarRut() de la clase Persona")
    print("=" * 70)

    exitos = 0
    fallos = 0

    for rut, esperado, descripcion in casos_de_prueba:
        persona = Persona(
            rut=rut,
            nombres="Juan Carlos",
            apellidoPaterno="Pérez",
            apellidoMaterno="González",
            telefono="912345678",
            correoElectronico="juan.perez@example.com"
        )

        resultado = persona.validarRut()
        paso = (resultado == esperado)

        if paso:
            exitos += 1
            estado = "✅ PASÓ"
        else:
            fallos += 1
            estado = "❌ FALLÓ"

        print(f"{estado} | RUT: {rut:<15} | Esperado: {str(esperado):<5} | Obtenido: {str(resultado):<5} | ({descripcion})")

    print("=" * 70)
    print(f"📊 RESUMEN RUT: {exitos} exitosas, {fallos} fallidas de {len(casos_de_prueba)} pruebas totales.")
    print("=" * 70)

def probar_validar_telefono():
    casos = [
        ("+56 9 1234 5678", True, "Teléfono chileno con prefijo"),
        ("912345678", True, "Teléfono 9 dígitos"),
        ("1234", False, "Teléfono muy corto"),
        ("", False, "Teléfono vacío"),
    ]
    print("\n" + "=" * 70)
    print(" 🧪 PRUEBAS UNITARIAS: Método validarTelefono() de la clase Persona")
    print("=" * 70)
    for tel, esp, desc in casos:
        p = Persona("12.345.678-5", "Juan", "Pérez", "Gómez", tel, "juan@email.com")
        res = p.validarTelefono()
        estado = "✅ PASÓ" if res == esp else "❌ FALLÓ"
        print(f"{estado} | Teléfono: {tel:<15} | Esperado: {str(esp):<5} | Obtenido: {str(res):<5} | ({desc})")

def probar_validar_correo():
    casos = [
        ("juan.perez@example.com", True, "Correo válido estándar"),
        ("contacto@powerfit.cl", True, "Correo válido dominio corto"),
        ("correo_invalido.com", False, "Correo sin arroba"),
        ("juan@", False, "Correo sin dominio"),
        ("", False, "Correo vacío"),
    ]
    print("\n" + "=" * 70)
    print(" 🧪 PRUEBAS UNITARIAS: Método validarCorreoElectronico() de la clase Persona")
    print("=" * 70)
    for correo, esp, desc in casos:
        p = Persona("12.345.678-5", "Juan", "Pérez", "Gómez", "912345678", correo)
        res = p.validarCorreoElectronico()
        estado = "✅ PASÓ" if res == esp else "❌ FALLÓ"
        print(f"{estado} | Correo: {correo:<25} | Esperado: {str(esp):<5} | Obtenido: {str(res):<5} | ({desc})")

if __name__ == "__main__":
    probar_validar_rut()
    probar_validar_telefono()
    probar_validar_correo()