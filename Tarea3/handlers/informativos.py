"""Comandos informativos: /hola, /hora, /contacto, /integrantes, /ayuda.

Responsable: Integrante 2  (TODO: colocar nombre y carnet)

Las funciones `texto_*` devuelven el mensaje como str para poder probarlas sin
Telegram; los handlers solo las envian. Los datos del grupo se centralizan en
las constantes de la parte superior para que sea facil completarlos.
"""

from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

# --------------------------------------------------------------------------- #
# Datos del grupo
# --------------------------------------------------------------------------- #
NOMBRE_GRUPO = "Grupo 6 - Inteligencia Artificial 1"
CURSO = "Inteligencia Artificial 1 - Seccion A"
UNIVERSIDAD = "Universidad de San Carlos de Guatemala"
FACULTAD = "Facultad de Ingenieria - Escuela de Ciencias y Sistemas"
REPOSITORIO = "https://github.com/andrekss/IA1_Tareas_2S2026_SECA"
CORREO_CONTACTO = "3031294090108@ingenieria.usac.edu.gt"

# (nombre, carnet) en el orden de los integrantes del README.
INTEGRANTES = (
    ("Evelio Marcos Josue Cruz Solliz", "202010040"),
    ("Andrés Alejandro Agosto Méndez", "202113580"),
    ("Daniel Hernandez", "202300512"),
    ("Jose Emanuel Monzon Lemus", "202300539"),
    ("Angel Geovanny Ordón Colchaj", "201905741"),
)

# (comando, sintaxis o None, descripcion, ejemplo o None)
COMANDOS_AYUDA = (
    ("hola", None, "Saluda utilizando tu nombre de Telegram.", None),
    ("hora", None, "Fecha y hora actual.", None),
    ("contacto", None, "Informacion de contacto del grupo.", None),
    ("integrantes", None, "Nombre y carnet de los integrantes.", None),
    ("ayuda", None, "Muestra esta lista de comandos.", None),
    ("menu", None, "Menu interactivo con botones.", None),
    (
        "calcular",
        "<numero1> <operador> <numero2>",
        "Suma, resta, multiplicacion o division.",
        "/calcular 15 + 3",
    ),
    ("tabla", "<numero>", "Tabla de multiplicar del 1 al 10.", "/tabla 7"),
    (
        "convertir",
        "<cantidad> <origen> <destino>",
        "Conversion de longitud entre cm, m, km, mi y ft.",
        "/convertir 5 km mi",
    ),
    ("aleatorio", "<min> <max>", "Entero aleatorio en el rango indicado.", "/aleatorio 1 100"),
)

DIAS = ("lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo")
MESES = (
    "enero", "febrero", "marzo", "abril", "mayo", "junio",
    "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
)


# --------------------------------------------------------------------------- #
# Generacion de textos (sin dependencias de Telegram)
# --------------------------------------------------------------------------- #
def texto_hola(nombre: str | None, username: str | None = None) -> str:
    """Saludo personalizado. Se envia sin Markdown porque el nombre lo define el usuario."""
    quien = nombre or (f"@{username}" if username else "usuario")
    return (
        f"Hola, {quien}! 👋\n\n"
        f"Bienvenido al bot de {NOMBRE_GRUPO}.\n"
        "Usa /menu para navegar con botones o /ayuda para ver todos los comandos."
    )


def _ahora() -> tuple[datetime, str]:
    """Fecha y hora actual en la zona configurada; si no existe, se usa UTC."""
    try:
        from config import settings

        nombre_zona = settings.ZONA_HORARIA
    except ImportError:  # Ejecucion directa de este archivo para pruebas.
        nombre_zona = "America/Guatemala"

    try:
        return datetime.now(ZoneInfo(nombre_zona)), nombre_zona
    except ZoneInfoNotFoundError:
        return datetime.now(ZoneInfo("UTC")), "UTC"


def texto_hora() -> str:
    ahora, zona = _ahora()
    fecha = f"{DIAS[ahora.weekday()]} {ahora.day} de {MESES[ahora.month - 1]} de {ahora.year}"
    return (
        "🕒 *Fecha y hora actual*\n\n"
        f"Fecha: {fecha.capitalize()}\n"
        f"Hora: `{ahora.strftime('%H:%M:%S')}`\n"
        f"Zona horaria: {zona}"
    )


def texto_contacto() -> str:
    return (
        "📞 *Contacto del grupo*\n\n"
        f"Grupo: {NOMBRE_GRUPO}\n"
        f"Curso: {CURSO}\n"
        f"{UNIVERSIDAD}\n"
        f"{FACULTAD}\n\n"
        f"Correo: {CORREO_CONTACTO}\n"
        f"Repositorio: [ver en GitHub]({REPOSITORIO})"
    )


def texto_integrantes() -> str:
    lineas = ["👥 *Integrantes del grupo*", ""]
    for indice, (nombre, carnet) in enumerate(INTEGRANTES, start=1):
        lineas.append(f"{indice}. {nombre} - `{carnet}`")
    return "\n".join(lineas)


def texto_ayuda() -> str:
    lineas = ["❓ *Comandos disponibles*", ""]
    for comando, sintaxis, descripcion, ejemplo in COMANDOS_AYUDA:
        encabezado = f"/{comando} {sintaxis}" if sintaxis else f"/{comando}"
        lineas.append(f"`{encabezado}`")
        lineas.append(f"   {descripcion}")
        if ejemplo:
            lineas.append(f"   Ejemplo: `{ejemplo}`")
    lineas += ["", "Los comandos con parametros validan la entrada y muestran la sintaxis correcta ante un error."]
    return "\n".join(lineas)


# --------------------------------------------------------------------------- #
# Handlers registrados en main.py
# --------------------------------------------------------------------------- #
async def hola(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    usuario = update.effective_user
    await update.message.reply_text(texto_hola(usuario.first_name, usuario.username))


async def hora(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(texto_hora(), parse_mode=ParseMode.MARKDOWN)


async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        texto_contacto(), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True
    )


async def integrantes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(texto_integrantes(), parse_mode=ParseMode.MARKDOWN)


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(texto_ayuda(), parse_mode=ParseMode.MARKDOWN)


if __name__ == "__main__":
    print(texto_hola("Daniel"))
    print("-" * 40)
    print(texto_hola(None, "usuario_x"))
    print("-" * 40)
    print(texto_hora())
    print("-" * 40)
    print(texto_contacto())
    print("-" * 40)
    print(texto_integrantes())
    print("-" * 40)
    print(texto_ayuda())
