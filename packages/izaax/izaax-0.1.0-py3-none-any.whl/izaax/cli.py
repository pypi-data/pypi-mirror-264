from __future__ import annotations

from dotenv import find_dotenv
from dotenv import load_dotenv

from .bot import IzaaxBot


def main() -> None:
    load_dotenv(find_dotenv())

    bot = IzaaxBot.from_env()
    bot.run()
