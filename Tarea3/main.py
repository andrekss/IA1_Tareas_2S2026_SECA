"""Punto de entrada del bot de Telegram - Tarea 03.

Arquitectura base y arranque.
Responsable: Evelio Marcos Josue Cruz Solliz (202010040)

Cada comando vive en su propio modulo dentro de handlers/. Este archivo solo
registra los handlers, por lo que los demas integrantes no necesitan editarlo.
"""

import logging

from telegram import BotCommand
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    MessageHandler,
    filters,
)

from config import settings
from handlers import comandos_matematicas, global_handler, informativos, menu, utilidades

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, settings.LOG_LEVEL, logging.INFO),
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

COMANDOS = [
    BotCommand("hola", "Saluda al usuario por su nombre"),
    BotCommand("hora", "Muestra la fecha y hora actual"),
    BotCommand("contacto", "Informacion de contacto del grupo"),
    BotCommand("integrantes", "Nombres y carnets de los integrantes"),
    BotCommand("ayuda", "Lista de comandos disponibles"),
    BotCommand("menu", "Menu interactivo con botones"),
    BotCommand("calcular", "Operacion aritmetica: <n1> <operador> <n2>"),
    BotCommand("tabla", "Tabla de multiplicar del 1 al 10: <numero>"),
    BotCommand("convertir", "Convierte longitudes: <cantidad> <origen> <destino>"),
    BotCommand("aleatorio", "Numero entero aleatorio: <min> <max>"),
]


async def _registrar_menu_comandos(application: Application) -> None:
    """Publica la lista de comandos que Telegram muestra al escribir '/'."""
    await application.bot.set_my_commands(COMANDOS)
    logger.info("Lista de comandos registrada en Telegram.")


def construir_aplicacion() -> Application:
    application = (
        ApplicationBuilder()
        .token(settings.TELEGRAM_TOKEN)
        .post_init(_registrar_menu_comandos)
        .build()
    )

    # Integrante 2 - comandos informativos
    application.add_handler(CommandHandler("start", informativos.hola))
    application.add_handler(CommandHandler("hola", informativos.hola))
    application.add_handler(CommandHandler("hora", informativos.hora))
    application.add_handler(CommandHandler("contacto", informativos.contacto))
    application.add_handler(CommandHandler("integrantes", informativos.integrantes))
    application.add_handler(CommandHandler("ayuda", informativos.ayuda))

    # Integrante 3 - menu interactivo
    application.add_handler(CommandHandler("menu", menu.menu))
    application.add_handler(CallbackQueryHandler(menu.manejar_boton))

    # Integrante 4 - modulo matematico
    application.add_handler(CommandHandler("calcular", comandos_matematicas.calcular))
    application.add_handler(CommandHandler("tabla", comandos_matematicas.tabla))

    # Integrante 5 - conversiones y aleatorios
    application.add_handler(CommandHandler("convertir", utilidades.convertir))
    application.add_handler(CommandHandler("aleatorio", utilidades.aleatorio))

    # Integrante 1 - manejo global (debe registrarse de ultimo)
    application.add_handler(
        MessageHandler(filters.COMMAND, global_handler.comando_desconocido)
    )
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, global_handler.texto_no_reconocido)
    )
    application.add_error_handler(global_handler.manejar_error)

    return application


def main() -> None:
    settings.validar_configuracion()
    logger.info("Iniciando bot de Telegram...")
    construir_aplicacion().run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
