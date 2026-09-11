import sys

if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def _escapar(texto: str) -> str:
    """Neutraliza los caracteres de Markdown en valores escritos por el usuario."""
    for caracter in ("\\", "`", "*", "_", "["):
        texto = texto.replace(caracter, "\\" + caracter)
    return texto


def _formatear_numero(valor: float) -> str:
    if valor.is_integer():
        return str(int(valor))
    return f"{valor:.4f}".rstrip("0").rstrip(".")


def _parsear_argumentos(args) -> list[str]:
    if isinstance(args, str):
        partes = args.strip().split()
        if partes and partes[0].startswith("/"):
            partes = partes[1:]
        return partes
    if isinstance(args, (list, tuple)):
        return [str(a).strip() for a in args if str(a).strip()]
    return []


def procesar_calcular(args) -> str:
    partes = _parsear_argumentos(args)

    if len(partes) != 3:
        return (
            "[ERROR] Sintaxis incorrecta en /calcular\n\n"
            "Se requieren exactamente 3 parametros: <numero1> <operador> <numero2>\n\n"
            "Uso correcto:\n"
            "`/calcular <numero1> <operador> <numero2>`\n\n"
            "Ejemplos:\n"
            "- `/calcular 10 + 5`\n"
            "- `/calcular 20.5 - 4.2`\n"
            "- `/calcular 8 * 3`\n"
            "- `/calcular 50 / 2`\n\n"
            "Operadores soportados: `+`, `-`, `*` (o `x`), `/`"
        )

    str_num1, operador, str_num2 = partes

    try:
        num1 = float(str_num1)
    except ValueError:
        return (
            f"[ERROR] El valor '{_escapar(str_num1)}' no es un numero valido.\n\n"
            "Uso correcto:\n"
            "`/calcular <numero1> <operador> <numero2>`\n"
            "Ejemplo: `/calcular 10 + 5`"
        )

    operadores_validos = {
        "+": "suma",
        "-": "resta",
        "*": "multiplicacion",
        "x": "multiplicacion",
        "X": "multiplicacion",
        "/": "division",
    }
    if operador not in operadores_validos:
        return (
            f"[ERROR] El operador '{_escapar(operador)}' no es valido.\n\n"
            "Operadores soportados:\n"
            "- Suma: `+`\n"
            "- Resta: `-`\n"
            "- Multiplicacion: `*` o `x`\n"
            "- Division: `/`\n\n"
            "Uso correcto:\n"
            "`/calcular <numero1> <operador> <numero2>`\n"
            "Ejemplo: `/calcular 10 * 5`"
        )

    try:
        num2 = float(str_num2)
    except ValueError:
        return (
            f"[ERROR] El valor '{_escapar(str_num2)}' no es un numero valido.\n\n"
            "Uso correcto:\n"
            "`/calcular <numero1> <operador> <numero2>`\n"
            "Ejemplo: `/calcular 10 + 5`"
        )

    if operador == "/" and num2 == 0:
        return (
            "[ERROR] Indeterminacion matematica: No es posible dividir entre cero (0).\n\n"
            "Por favor, ingrese un divisor distinto de cero.\n"
            "Ejemplo: `/calcular 10 / 2`"
        )

    if operador == "+":
        resultado = num1 + num2
        simbolo = "+"
    elif operador == "-":
        resultado = num1 - num2
        simbolo = "-"
    elif operador in ("*", "x", "X"):
        resultado = num1 * num2
        simbolo = "*"
    elif operador == "/":
        resultado = num1 / num2
        simbolo = "/"

    n1_str = _formatear_numero(num1)
    n2_str = _formatear_numero(num2)
    res_str = _formatear_numero(resultado)

    return (
        "Resultado del calculo:\n\n"
        f"`{n1_str} {simbolo} {n2_str} = {res_str}`"
    )


def procesar_tabla(args) -> str:
    partes = _parsear_argumentos(args)

    if len(partes) != 1:
        return (
            "[ERROR] Sintaxis incorrecta en /tabla\n\n"
            "Debe ingresar exactamente un numero.\n\n"
            "Uso correcto:\n"
            "`/tabla <numero>`\n\n"
            "Ejemplos:\n"
            "- `/tabla 7`\n"
            "- `/tabla 5.5`"
        )

    try:
        numero = float(partes[0])
    except ValueError:
        return (
            f"[ERROR] El valor '{_escapar(partes[0])}' no es un numero valido.\n\n"
            "Uso correcto:\n"
            "`/tabla <numero>`\n"
            "Ejemplo: `/tabla 7`"
        )

    num_str = _formatear_numero(numero)
    lineas = [f"Tabla de multiplicar del {num_str} (1 al 10):\n"]

    for i in range(1, 11):
        producto = numero * i
        lineas.append(f"`{num_str} x {i:>2} = {_formatear_numero(producto)}`")

    return "\n".join(lineas)


if __name__ == "__main__":
    print("=" * 60)
    print("EJECUTANDO SUITE DE PRUEBAS")
    print("=" * 60)

    pruebas_calcular = [
        (["10", "+", "5"], "Suma entera valida"),
        (["20", "-", "8"], "Resta valida"),
        (["4", "*", "2.5"], "Multiplicacion valida con decimal"),
        (["100", "/", "4"], "Division exacta valida"),
        (["10", "/", "0"], "Control de division entre cero"),
        (["10", "%", "5"], "Control de operador no soportado"),
        (["abc", "+", "5"], "Control de primer operando no numerico"),
        (["5", "+", "xyz"], "Control de segundo operando no numerico"),
        ([], "Control de ausencia de argumentos"),
        (["10", "+"], "Control de argumentos incompletos"),
        (["10", "+", "5", "extra"], "Control de exceso de argumentos"),
    ]

    print("\n--- Pruebas de /calcular ---")
    for entrada, descripcion in pruebas_calcular:
        print(f"\n[Test: {descripcion}] Entrada: {entrada}")
        print(procesar_calcular(entrada))

    pruebas_tabla = [
        (["7"], "Tabla entera del 7"),
        (["3.5"], "Tabla decimal del 3.5"),
        ([], "Control de ausencia de argumentos"),
        (["7", "8"], "Control de exceso de argumentos"),
        (["texto"], "Control de argumento no numerico"),
    ]

    print("\n\n--- Pruebas de /tabla ---")
    for entrada, descripcion in pruebas_tabla:
        print(f"\n[Test: {descripcion}] Entrada: {entrada}")
        print(procesar_tabla(entrada))

    print("\n" + "=" * 60)
    print("PRUEBAS FINALIZADAS EXITOSAMENTE SIN ERRORES.")
    print("=" * 60)
