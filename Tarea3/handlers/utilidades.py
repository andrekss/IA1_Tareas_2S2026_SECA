"""Conversiones de longitud y numeros aleatorios: /convertir, /aleatorio.

Responsable: Integrante 5  (TODO: colocar nombre y carnet)

Sugerencia: siga el patron del modulo matematicas.py, es decir funciones puras
que reciban `context.args` y devuelvan un str, para poder probarlas sin Telegram.
"""

from telegram import Update
from telegram.ext import ContextTypes


async def convertir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO Integrante 5: conversion entre cm, m, km, mi, ft con validaciones
    await update.message.reply_text("[PENDIENTE] /convertir aun no ha sido implementado.")


async def aleatorio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # TODO Integrante 5: entero aleatorio en el rango cerrado [min, max]
    await update.message.reply_text("[PENDIENTE] /aleatorio aun no ha sido implementado.")
