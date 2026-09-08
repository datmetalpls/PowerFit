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
    print(f"📊 RESUMEN: {exitos} exitosas, {fallos} fallidas de {len(casos_de_prueba)} pruebas totales.")
    print("=" * 70)

if __name__ == "__main__":
    probar_validar_rut()