"""Comandos informativos: /hola, /hora, /contacto, /integrantes, /ayuda.

Responsable: Integrante 2  (TODO: colocar nombre y carnet)

Cada funcion debe responder con `await update.message.reply_text(...)`.
No es necesario registrar nada en main.py: los handlers ya estan cableados.
"""

from telegram import Update
from telegram.ext import ContextTypes


async def hola(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO Integrante 2: saludar usando update.effective_user.first_name
    await update.message.reply_text("[PENDIENTE] /hola aun no ha sido implementado.")


async def hora(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO Integrante 2: fecha y hora actual con zona horaria settings.ZONA_HORARIA
    await update.message.reply_text("[PENDIENTE] /hora aun no ha sido implementado.")


async def contacto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO Integrante 2: datos de contacto del grupo
    await update.message.reply_text("[PENDIENTE] /contacto aun no ha sido implementado.")


async def integrantes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO Integrante 2: nombre y carnet de los 5 integrantes
    await update.message.reply_text("[PENDIENTE] /integrantes aun no ha sido implementado.")


async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO Integrante 2: lista de comandos con descripcion y sintaxis
    await update.message.reply_text("[PENDIENTE] /ayuda aun no ha sido implementado.")
