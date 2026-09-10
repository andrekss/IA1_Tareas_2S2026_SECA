"""Adaptador de Telegram para el modulo matematico.

Responsable del adaptador: Evelio Marcos Josue Cruz Solliz (202010040)
Logica de calculo: Jose Emanuel Monzon Lemus (202300539) en handlers/matematicas.py

Se mantiene matematicas.py libre de dependencias de Telegram para conservar su
suite de pruebas local.
"""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from handlers.matematicas import procesar_calcular, procesar_tabla


async def calcular(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        procesar_calcular(context.args), parse_mode=ParseMode.MARKDOWN
    )


async def tabla(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        procesar_tabla(context.args), parse_mode=ParseMode.MARKDOWN
    )
