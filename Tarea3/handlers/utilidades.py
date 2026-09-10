"""Conversiones de longitud y numeros aleatorios: /convertir, /aleatorio.

Responsable: Integrante 5  (TODO: colocar nombre y carnet)

Sigue el patron de matematicas.py: `procesar_convertir` y `procesar_aleatorio`
son funciones puras que reciben `context.args` y devuelven un str, por lo que
se prueban sin Telegram con `python handlers/utilidades.py`.
"""

import random

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

# Factor para llevar cada unidad a metros.
FACTORES_A_METROS = {
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
    "mi": 1609.344,
    "ft": 0.3048,
}

NOMBRES_UNIDADES = {
    "cm": "centimetros",
    "m": "metros",
    "km": "kilometros",
    "mi": "millas",
    "ft": "pies",
}

UNIDADES_TEXTO = ", ".join(f"`{u}`" for u in FACTORES_A_METROS)

USO_CONVERTIR = (
    "Uso correcto:\n"
    "`/convertir <cantidad> <unidad origen> <unidad destino>`\n\n"
    "Ejemplos:\n"
    "- `/convertir 5 km mi`\n"
    "- `/convertir 100 cm m`\n"
    "- `/convertir 3 ft cm`\n\n"
    f"Unidades soportadas: {UNIDADES_TEXTO}"
)

USO_ALEATORIO = (
    "Uso correcto:\n"
    "`/aleatorio <min> <max>`\n\n"
    "Ejemplos:\n"
    "- `/aleatorio 1 100`\n"
    "- `/aleatorio -10 10`\n\n"
    "Ambos limites deben ser numeros enteros y min debe ser menor o igual que max."
)


def _escapar(texto: str) -> str:
    """Neutraliza los caracteres de Markdown en valores escritos por el usuario."""
    for caracter in ("\\", "`", "*", "_", "["):
        texto = texto.replace(caracter, "\\" + caracter)
    return texto


def _formatear_numero(valor: float) -> str:
    if valor.is_integer():
        return str(int(valor))
    return f"{valor:.6f}".rstrip("0").rstrip(".")


def _parsear_argumentos(args) -> list[str]:
    if isinstance(args, str):
        partes = args.strip().split()
        if partes and partes[0].startswith("/"):
            partes = partes[1:]
        return partes
    if isinstance(args, (list, tuple)):
        return [str(a).strip() for a in args if str(a).strip()]
    return []


# --------------------------------------------------------------------------- #
# /convertir
# --------------------------------------------------------------------------- #
def procesar_convertir(args) -> str:
    partes = _parsear_argumentos(args)

    if len(partes) != 3:
        return (
            "[ERROR] Sintaxis incorrecta en /convertir\n\n"
            "Se requieren exactamente 3 parametros: "
            "<cantidad> <unidad origen> <unidad destino>\n\n" + USO_CONVERTIR
        )

    str_cantidad, str_origen, str_destino = partes

    try:
        cantidad = float(str_cantidad)
    except ValueError:
        return f"[ERROR] La cantidad '{_escapar(str_cantidad)}' no es un numero valido.\n\n" + USO_CONVERTIR

    if cantidad != cantidad or cantidad in (float("inf"), float("-inf")):
        return f"[ERROR] La cantidad '{_escapar(str_cantidad)}' no es un numero valido.\n\n" + USO_CONVERTIR

    if cantidad < 0:
        return (
            "[ERROR] La cantidad no puede ser negativa.\n\n"
            "Ingrese un valor mayor o igual a cero.\n"
            "Ejemplo: `/convertir 5 km mi`"
        )

    origen = str_origen.lower()
    destino = str_destino.lower()

    for etiqueta, unidad, original in (("origen", origen, str_origen), ("destino", destino, str_destino)):
        if unidad not in FACTORES_A_METROS:
            return (
                f"[ERROR] La unidad de {etiqueta} '{_escapar(original)}' no es valida.\n\n"
                f"Unidades soportadas: {UNIDADES_TEXTO}\n\n"
                "Uso correcto:\n"
                "`/convertir <cantidad> <unidad origen> <unidad destino>`\n"
                "Ejemplo: `/convertir 5 km mi`"
            )

    resultado = cantidad * FACTORES_A_METROS[origen] / FACTORES_A_METROS[destino]

    return (
        "Resultado de la conversion:\n\n"
        f"`{_formatear_numero(cantidad)} {origen} = {_formatear_numero(resultado)} {destino}`\n\n"
        f"({NOMBRES_UNIDADES[origen]} a {NOMBRES_UNIDADES[destino]})"
    )


# --------------------------------------------------------------------------- #
# /aleatorio
# --------------------------------------------------------------------------- #
def _parsear_entero(texto: str) -> int:
    """Acepta enteros con signo; rechaza decimales y texto."""
    return int(texto)


def procesar_aleatorio(args, generador=random.randint) -> str:
    partes = _parsear_argumentos(args)

    if len(partes) != 2:
        return (
            "[ERROR] Sintaxis incorrecta en /aleatorio\n\n"
            "Se requieren exactamente 2 parametros: <min> <max>\n\n" + USO_ALEATORIO
        )

    valores = []
    for etiqueta, texto in (("min", partes[0]), ("max", partes[1])):
        try:
            valores.append(_parsear_entero(texto))
        except ValueError:
            return (
                f"[ERROR] El valor de {etiqueta} '{_escapar(texto)}' no es un numero entero valido.\n\n"
                + USO_ALEATORIO
            )

    minimo, maximo = valores
    if minimo > maximo:
        return (
            f"[ERROR] El minimo ({minimo}) no puede ser mayor que el maximo ({maximo}).\n\n"
            "Ejemplo: `/aleatorio 1 100`"
        )

    numero = generador(minimo, maximo)
    return (
        "Numero aleatorio generado:\n\n"
        f"`{numero}`\n\n"
        f"(rango [{minimo}, {maximo}])"
    )


# --------------------------------------------------------------------------- #
# Handlers registrados en main.py
# --------------------------------------------------------------------------- #
async def convertir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        procesar_convertir(context.args), parse_mode=ParseMode.MARKDOWN
    )


async def aleatorio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        procesar_aleatorio(context.args), parse_mode=ParseMode.MARKDOWN
    )


if __name__ == "__main__":
    print("=" * 60)
    print("EJECUTANDO SUITE DE PRUEBAS DE UTILIDADES")
    print("=" * 60)

    pruebas_convertir = [
        (["5", "km", "mi"], "Kilometros a millas", "3.106856 mi"),
        (["100", "cm", "m"], "Centimetros a metros", "= 1 m"),
        (["3", "ft", "cm"], "Pies a centimetros", "= 91.44 cm"),
        (["1", "mi", "km"], "Millas a kilometros", "= 1.609344 km"),
        (["2.5", "M", "FT"], "Unidades en mayusculas", "= 8.2021 ft"),
        (["0", "km", "m"], "Cantidad cero", "= 0 m"),
        (["-5", "km", "m"], "Control de cantidad negativa", "[ERROR]"),
        (["abc", "km", "m"], "Control de cantidad no numerica", "[ERROR]"),
        (["5", "yd", "m"], "Control de unidad origen invalida", "[ERROR]"),
        (["5", "km", "pulg"], "Control de unidad destino invalida", "[ERROR]"),
        ([], "Control de ausencia de argumentos", "[ERROR]"),
        (["5", "km"], "Control de argumentos incompletos", "[ERROR]"),
        (["5", "km", "mi", "extra"], "Control de exceso de argumentos", "[ERROR]"),
    ]

    print("\n--- Pruebas de /convertir ---")
    for entrada, descripcion, esperado in pruebas_convertir:
        salida = procesar_convertir(entrada)
        print(f"\n[Test: {descripcion}] Entrada: {entrada}")
        print(salida)
        assert esperado in salida, f"Se esperaba '{esperado}' en la salida"

    pruebas_aleatorio = [
        (["1", "100"], "Rango valido", None),
        (["-10", "10"], "Rango con negativos", None),
        (["7", "7"], "Min igual a max", "`7`"),
        (["10", "1"], "Control de min mayor que max", "[ERROR]"),
        (["1.5", "10"], "Control de decimal en min", "[ERROR]"),
        (["1", "diez"], "Control de texto en max", "[ERROR]"),
        ([], "Control de ausencia de argumentos", "[ERROR]"),
        (["5"], "Control de argumentos incompletos", "[ERROR]"),
        (["1", "2", "3"], "Control de exceso de argumentos", "[ERROR]"),
    ]

    print("\n\n--- Pruebas de /aleatorio ---")
    for entrada, descripcion, esperado in pruebas_aleatorio:
        salida = procesar_aleatorio(entrada)
        print(f"\n[Test: {descripcion}] Entrada: {entrada}")
        print(salida)
        if esperado:
            assert esperado in salida, f"Se esperaba '{esperado}' en la salida"
        else:
            assert "[ERROR]" not in salida

    # El numero generado debe caer dentro del rango cerrado.
    for _ in range(200):
        salida = procesar_aleatorio(["-3", "3"])
        numero = int(salida.split("`")[1])
        assert -3 <= numero <= 3, numero

    print("\n" + "=" * 60)
    print("PRUEBAS FINALIZADAS EXITOSAMENTE SIN ERRORES.")
    print("=" * 60)
