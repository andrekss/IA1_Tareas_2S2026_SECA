"""Menu interactivo con botones de Telegram: /menu.

Responsable: Integrante 3  (TODO: colocar nombre y carnet)

`menu` responde al comando /menu.
`manejar_boton` recibe los callbacks de los botones; ya esta registrado como
CallbackQueryHandler en main.py, no hace falta tocar ese archivo.
"""

from telegram import Update
from telegram.ext import ContextTypes


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO Integrante 3: construir InlineKeyboardMarkup con las categorias
    await update.message.reply_text("[PENDIENTE] /menu aun no ha sido implementado.")


async def manejar_boton(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO Integrante 3: despachar segun query.data e incluir "Volver al Menu"
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("[PENDIENTE] El menu interactivo aun no responde.")
