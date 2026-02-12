from telethon import TelegramClient
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
CHANNEL = "@CumtaAlertsEnglishChannel"


async def get_oldest_message():
    async with TelegramClient("cumta_test", API_ID, API_HASH) as client:
        # fetching 1 message from the very start
        async for message in client.iter_messages(CHANNEL, limit=1, reverse=True):
            print("Oldest message id:", message.id)
            print("Date:", message.date)
            if message.text:
                print("Text preview:", message.text[:100])
            else:
                print("No text content in this message")


if __name__ == "__main__":
    asyncio.run(get_oldest_message())


# Oldest message id: 1
# Date: 2018-12-26 10:05:01+00:00
