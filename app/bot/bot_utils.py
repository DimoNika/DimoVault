from telebot.async_telebot import AsyncTeleBot
from .bot_config import TOKEN

# bot = AsyncTeleBot("7338534439:AAHDCPaKSUEc3eitG4FMgRrSnrRJEWy3E3E")
bot = AsyncTeleBot(TOKEN)




async def test_send_message():
    await bot.send_message(844162808, "hello world")