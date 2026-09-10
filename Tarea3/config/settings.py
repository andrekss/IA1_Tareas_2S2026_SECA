"""Carga y validacion de variables de entorno del bot.

Responsable: Evelio Marcos Josue Cruz Solliz (202010040)
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ZONA_HORARIA = os.getenv("ZONA_HORARIA", "America/Guatemala")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def validar_configuracion() -> None:
    """Detiene el arranque si falta el token en lugar de fallar en tiempo de ejecucion."""
    if not TELEGRAM_TOKEN:
        print(
            "[ERROR] La variable de entorno TELEGRAM_TOKEN no esta definida.\n"
            "Cree un archivo .env a partir de .env.example y coloque el token "
            "entregado por BotFather.",
            file=sys.stderr,
        )
        sys.exit(1)
