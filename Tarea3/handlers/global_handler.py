"""Manejador global de comandos inexistentes, mensajes libres y excepciones.

Responsable: Evelio Marcos Josue Cruz Solliz (202010040)
"""

import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

MENSAJE_COMANDO_DESCONOCIDO = (
    "[ERROR] El comando ingresado no existe.\n\n"
    "Utilice /ayuda para consultar la lista de comandos disponibles "
    "o /menu para abrir el menu interactivo."
)

MENSAJE_TEXTO_LIBRE = (
    "No comprendo los mensajes de texto libre.\n\n"
    "Utilice /ayuda para consultar la lista de comandos disponibles "
    "o /menu para abrir el menu interactivo."
)


async def comando_desconocido(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(MENSAJE_COMANDO_DESCONOCIDO)


async def texto_no_reconocido(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(MENSAJE_TEXTO_LIBRE)


async def manejar_error(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Evita que una excepcion en cualquier handler detenga el bot."""
    logger.error("Excepcion no controlada", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(
            "[ERROR] Ocurrio un problema inesperado al procesar su solicitud.\n\n"
            "El bot sigue activo. Intente nuevamente o consulte /ayuda."
        )
