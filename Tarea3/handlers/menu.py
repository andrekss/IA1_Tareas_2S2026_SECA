"""Menu interactivo con botones de Telegram: /menu.

Responsable: Daniel Hernandez (202300512) - Integrante 3

Flujo de navegacion
-------------------
    /menu
      └── Menu principal (InlineKeyboardMarkup con 4 categorias)
            ├── Informacion   -> /hola /hora /contacto /integrantes /ayuda
            │                    (al presionar se EJECUTA el comando)
            ├── Calculos      -> /calcular /tabla
            ├── Conversiones  -> /convertir
            └── Utilidades    -> /aleatorio
                                 (al presionar se muestra la PLANTILLA de uso,
                                  con un boton "Probar ejemplo" que lo ejecuta)

Todas las pantallas que no son el menu principal incluyen el boton
"⬅️ Volver al Menu".

Los botones se identifican con `callback_data` de la forma:
    menu            -> menu principal
    cat:<clave>     -> pantalla de una categoria
    run:<comando>   -> ejecuta un comando sin parametros
    tpl:<comando>   -> muestra la plantilla de uso de un comando
    ej:<comando>    -> ejecuta el comando con los argumentos del ejemplo

`menu` responde al comando /menu y `manejar_boton` a todos los callbacks;
ambos ya estan registrados en main.py.
"""

import logging
from dataclasses import dataclass, field
from typing import Awaitable, Callable, Optional

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.error import BadRequest
from telegram.ext import ContextTypes

from handlers import comandos_matematicas, informativos, utilidades

logger = logging.getLogger(__name__)

Handler = Callable[[Update, ContextTypes.DEFAULT_TYPE], Awaitable[None]]

TEXTO_VOLVER = "⬅️ Volver al Menú"
CALLBACK_MENU = "menu"


# --------------------------------------------------------------------------- #
# Definicion declarativa del menu
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Opcion:
    """Un comando del bot expuesto como boton del menu."""

    comando: str
    etiqueta: str
    descripcion: str
    handler: Handler
    parametros: Optional[str] = None
    ejemplos: tuple[str, ...] = field(default_factory=tuple)
    notas: tuple[str, ...] = field(default_factory=tuple)

    @property
    def tiene_parametros(self) -> bool:
        return self.parametros is not None

    @property
    def args_ejemplo(self) -> list[str]:
        """Argumentos del primer ejemplo, listos para `context.args`."""
        return self.ejemplos[0].split() if self.ejemplos else []


@dataclass(frozen=True)
class Categoria:
    clave: str
    titulo: str
    descripcion: str
    comandos: tuple[str, ...]


OPCIONES: dict[str, Opcion] = {
    "hola": Opcion(
        comando="hola",
        etiqueta="👋 Saludar",
        descripcion="Saluda al usuario utilizando su nombre de Telegram.",
        handler=informativos.hola,
    ),
    "hora": Opcion(
        comando="hora",
        etiqueta="🕒 Fecha y hora",
        descripcion="Muestra la fecha y hora actual.",
        handler=informativos.hora,
    ),
    "contacto": Opcion(
        comando="contacto",
        etiqueta="📞 Contacto",
        descripcion="Informacion de contacto del grupo.",
        handler=informativos.contacto,
    ),
    "integrantes": Opcion(
        comando="integrantes",
        etiqueta="👥 Integrantes",
        descripcion="Nombre y carnet de los integrantes.",
        handler=informativos.integrantes,
    ),
    "ayuda": Opcion(
        comando="ayuda",
        etiqueta="❓ Ayuda",
        descripcion="Lista de comandos disponibles.",
        handler=informativos.ayuda,
    ),
    "calcular": Opcion(
        comando="calcular",
        etiqueta="➕ Calcular",
        descripcion="Suma, resta, multiplicacion y division.",
        handler=comandos_matematicas.calcular,
        parametros="<numero1> <operador> <numero2>",
        ejemplos=("10 + 5", "20.5 - 4.2", "8 * 3", "50 / 2"),
        notas=("Operadores soportados: `+`, `-`, `*` (o `x`), `/`",),
    ),
    "tabla": Opcion(
        comando="tabla",
        etiqueta="✖️ Tabla de multiplicar",
        descripcion="Tabla de multiplicar del 1 al 10.",
        handler=comandos_matematicas.tabla,
        parametros="<numero>",
        ejemplos=("7", "12"),
    ),
    "convertir": Opcion(
        comando="convertir",
        etiqueta="📏 Convertir longitud",
        descripcion="Convierte entre unidades de longitud.",
        handler=utilidades.convertir,
        parametros="<cantidad> <unidad origen> <unidad destino>",
        ejemplos=("5 km mi", "100 cm m", "3 ft cm"),
        notas=("Unidades soportadas: cm, m, km, mi, ft",),
    ),
    "aleatorio": Opcion(
        comando="aleatorio",
        etiqueta="🎲 Numero aleatorio",
        descripcion="Entero aleatorio dentro de un rango.",
        handler=utilidades.aleatorio,
        parametros="<min> <max>",
        ejemplos=("1 100", "10 20"),
        notas=("Ambos limites deben ser enteros y min debe ser menor o igual que max.",),
    ),
}

CATEGORIAS: dict[str, Categoria] = {
    "info": Categoria(
        clave="info",
        titulo="ℹ️ Información",
        descripcion="Datos del bot y del grupo. Presiona una opción para ejecutarla.",
        comandos=("hola", "hora", "contacto", "integrantes", "ayuda"),
    ),
    "calc": Categoria(
        clave="calc",
        titulo="🧮 Cálculos",
        descripcion="Operaciones aritméticas y tablas de multiplicar.",
        comandos=("calcular", "tabla"),
    ),
    "conv": Categoria(
        clave="conv",
        titulo="📐 Conversiones",
        descripcion="Conversión entre unidades de longitud.",
        comandos=("convertir",),
    ),
    "util": Categoria(
        clave="util",
        titulo="🛠️ Utilidades",
        descripcion="Herramientas varias.",
        comandos=("aleatorio",),
    ),
}

_CATEGORIA_DE_COMANDO: dict[str, str] = {
    comando: categoria.clave
    for categoria in CATEGORIAS.values()
    for comando in categoria.comandos
}


# --------------------------------------------------------------------------- #
# Construccion de textos y teclados
# --------------------------------------------------------------------------- #
def _boton_volver() -> InlineKeyboardButton:
    return InlineKeyboardButton(TEXTO_VOLVER, callback_data=CALLBACK_MENU)


def texto_menu_principal() -> str:
    return (
        "📋 *Menú principal*\n\n"
        "Selecciona una categoría para ver las opciones disponibles.\n"
        "También puedes escribir los comandos directamente; usa /ayuda para "
        "ver la lista completa."
    )


def teclado_menu_principal() -> InlineKeyboardMarkup:
    claves = list(CATEGORIAS)
    filas = [
        [
            InlineKeyboardButton(CATEGORIAS[clave].titulo, callback_data=f"cat:{clave}")
            for clave in claves[i : i + 2]
        ]
        for i in range(0, len(claves), 2)
    ]
    return InlineKeyboardMarkup(filas)


def texto_categoria(categoria: Categoria) -> str:
    lineas = [f"*{categoria.titulo}*", "", categoria.descripcion, ""]
    for clave in categoria.comandos:
        opcion = OPCIONES[clave]
        lineas.append(f"• /{opcion.comando}: {opcion.descripcion}")
    return "\n".join(lineas)


def teclado_categoria(categoria: Categoria) -> InlineKeyboardMarkup:
    filas = []
    for clave in categoria.comandos:
        opcion = OPCIONES[clave]
        accion = "tpl" if opcion.tiene_parametros else "run"
        filas.append(
            [InlineKeyboardButton(opcion.etiqueta, callback_data=f"{accion}:{clave}")]
        )
    filas.append([_boton_volver()])
    return InlineKeyboardMarkup(filas)


def texto_plantilla(opcion: Opcion) -> str:
    lineas = [
        f"*{opcion.etiqueta}*",
        "",
        opcion.descripcion,
        "",
        "Uso:",
        f"`/{opcion.comando} {opcion.parametros}`",
    ]
    if opcion.ejemplos:
        lineas += ["", "Ejemplos:"]
        lineas += [f"• `/{opcion.comando} {ejemplo}`" for ejemplo in opcion.ejemplos]
    if opcion.notas:
        lineas += [""] + list(opcion.notas)
    lineas += [
        "",
        "Escribe el comando en el chat con tus propios valores o presiona "
        "*Probar ejemplo* para ejecutar el primero.",
    ]
    return "\n".join(lineas)


def teclado_plantilla(opcion: Opcion) -> InlineKeyboardMarkup:
    categoria = CATEGORIAS[_CATEGORIA_DE_COMANDO[opcion.comando]]
    filas = []
    if opcion.ejemplos:
        filas.append(
            [
                InlineKeyboardButton(
                    f"▶️ Probar ejemplo: /{opcion.comando} {opcion.ejemplos[0]}",
                    callback_data=f"ej:{opcion.comando}",
                )
            ]
        )
    filas.append(
        [
            InlineKeyboardButton(f"◀️ {categoria.titulo}", callback_data=f"cat:{categoria.clave}"),
            _boton_volver(),
        ]
    )
    return InlineKeyboardMarkup(filas)


# --------------------------------------------------------------------------- #
# Utilidades internas
# --------------------------------------------------------------------------- #
class _UpdateDesdeBoton:
    """Adapta un update de boton para reutilizar los handlers de comandos.

    Los handlers de los demas integrantes responden con `update.message`, que
    es None cuando el update proviene de un CallbackQuery. Este envoltorio
    expone el mensaje del menu como `message` y delega todo lo demas
    (`effective_user`, `effective_chat`, etc.) al update original, de modo que
    los comandos se ejecutan sin modificar sus modulos.
    """

    def __init__(self, update: Update) -> None:
        self._original = update
        self.message = update.effective_message

    def __getattr__(self, nombre: str):
        return getattr(self._original, nombre)


async def _mostrar(update: Update, texto: str, teclado: InlineKeyboardMarkup) -> None:
    """Edita el mensaje del menu en su lugar; si no es posible, envia uno nuevo."""
    query = update.callback_query
    try:
        await query.edit_message_text(
            texto, reply_markup=teclado, parse_mode=ParseMode.MARKDOWN
        )
    except BadRequest as exc:
        if "not modified" in str(exc).lower():
            return  # Se presiono el mismo boton dos veces: no hay nada que cambiar.
        logger.warning("No se pudo editar el mensaje del menu: %s", exc)
        await update.effective_chat.send_message(
            texto, reply_markup=teclado, parse_mode=ParseMode.MARKDOWN
        )


async def _ejecutar(
    update: Update, context: ContextTypes.DEFAULT_TYPE, opcion: Opcion, args: list[str]
) -> None:
    """Ejecuta el handler del comando y vuelve a colocar el menu al final del chat."""
    context.args = args
    await opcion.handler(_UpdateDesdeBoton(update), context)

    # El resultado quedo como un mensaje nuevo debajo del menu. Se deja
    # constancia en el mensaje anterior y se vuelve a enviar la categoria al
    # final del chat para que el usuario no tenga que desplazarse hacia arriba.
    categoria = CATEGORIAS[_CATEGORIA_DE_COMANDO[opcion.comando]]
    comando = f"/{opcion.comando} {' '.join(args)}".strip()
    try:
        await update.callback_query.edit_message_text(f"✅ Ejecutado: {comando}")
    except BadRequest as exc:
        logger.debug("No se pudo actualizar el menu anterior: %s", exc)
    await update.effective_chat.send_message(
        texto_categoria(categoria),
        reply_markup=teclado_categoria(categoria),
        parse_mode=ParseMode.MARKDOWN,
    )


# --------------------------------------------------------------------------- #
# Handlers registrados en main.py
# --------------------------------------------------------------------------- #
async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde a /menu con el menu principal."""
    await update.message.reply_text(
        texto_menu_principal(),
        reply_markup=teclado_menu_principal(),
        parse_mode=ParseMode.MARKDOWN,
    )


async def manejar_boton(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Despacha los callbacks de los botones segun su `callback_data`."""
    query = update.callback_query
    await query.answer()

    if update.effective_message is None:
        # El mensaje del menu es demasiado antiguo y Telegram ya no permite
        # editarlo: se envia un menu nuevo en lugar de fallar.
        await update.effective_chat.send_message(
            texto_menu_principal(),
            reply_markup=teclado_menu_principal(),
            parse_mode=ParseMode.MARKDOWN,
        )
        return

    data = query.data or ""
    accion, _, argumento = data.partition(":")

    if accion == "cat" and argumento in CATEGORIAS:
        categoria = CATEGORIAS[argumento]
        await _mostrar(update, texto_categoria(categoria), teclado_categoria(categoria))
        return

    if accion == "tpl" and argumento in OPCIONES:
        opcion = OPCIONES[argumento]
        await _mostrar(update, texto_plantilla(opcion), teclado_plantilla(opcion))
        return

    if accion == "run" and argumento in OPCIONES:
        await _ejecutar(update, context, OPCIONES[argumento], [])
        return

    if accion == "ej" and argumento in OPCIONES:
        opcion = OPCIONES[argumento]
        await _ejecutar(update, context, opcion, opcion.args_ejemplo)
        return

    if data != CALLBACK_MENU:
        # Boton desconocido (por ejemplo, de una version anterior del bot):
        # se regresa al menu principal en lugar de fallar.
        logger.warning("callback_data no reconocido: %r", data)
    await _mostrar(update, texto_menu_principal(), teclado_menu_principal())
