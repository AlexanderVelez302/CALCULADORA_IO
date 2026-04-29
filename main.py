from core.router import resolver

print("=== CALCULADORA IO ===")

while True:
    print("\nEscribe tu ejercicio (termina con FIN):")

    lineas = []
    while True:
        linea = input()
        if linea.strip().upper() == "FIN":
            break
        lineas.append(linea)

    pregunta = "\n".join(lineas)

    if pregunta.lower() == "salir":
        break

    resultado = resolver(pregunta)

    print("\nRESULTADO:")
    print(resultado)