from __future__ import annotations

import asyncio
import os

from redis import Redis
from telegram import Bot

from .client import IzaaxClient


class IzaaxBot:
    def __init__(self, client: IzaaxClient, bot: Bot, redis: Redis, chat_id: int):
        self.client = client
        self.bot = bot
        self.redis = redis
        self.chat_id = chat_id

    @classmethod
    def from_env(cls) -> IzaaxBot:
        client = IzaaxClient.from_env()

        token = os.getenv("BOT_TOKEN")
        if token is None:
            raise ValueError("BOT_TOKEN is not set")
        bot = Bot(token=token)

        redis = Redis()

        chat_id = os.getenv("BOT_CHAT_ID")
        if chat_id is None:
            raise ValueError("BOT_CHAT_ID is not set")

        return cls(client=client, bot=bot, redis=redis, chat_id=chat_id)

    async def arun(self) -> None:
        self.client.login()

        await self.bot.initialize()

        for item in self.client.read_rss():
            if not self.redis.exists(item.redis_key):
                await self.bot.send_message(chat_id=self.chat_id, text=f"{item.title}\n{item.link}")
                self.redis.set(item.redis_key, item.link)

        await self.bot.shutdown()

    def run(self) -> None:
        asyncio.run(self.arun())
