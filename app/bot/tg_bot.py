import os
from dotenv import load_dotenv
load_dotenv()

#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import asyncio

from telebot.async_telebot import AsyncTeleBot



bot = AsyncTeleBot(os.getenv("TG_BOT_TOKEN"))

import pymongo

#  adress from .env
dbclient = pymongo.MongoClient(os.getenv("DB_CONNECTION_STRING"))



db = dbclient["vault_db"]
# items_table = db["items"]
users_table = db["users"]




# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
async def send_welcome(message):
    print(message.from_user.username, "/start")
    text = 'Hi, I am VaultBot.\n\nType /register to connect bot.'
    await bot.reply_to(message, text)


# Handle '/help'
@bot.message_handler(commands=['help'])
async def send_welcome(message):
    print(message.from_user.username, "/help")

    text = 'Type /register to connect bot.'
    await bot.reply_to(message, text)

# Handle '/register'
@bot.message_handler(commands=['register'])
async def send_welcome(message):
        


    if users_table.find_one({"tg_username": message.from_user.username.lower()}):
        # await bot.send_message(message.from_user.id, users_table.find_one({"tg_username": message.from_user.username.lower()}))

        users_table.update_one({"tg_username": message.from_user.username.lower()}, {"$set": {"chat_id": message.from_user.id}})
        await bot.send_message(message.from_user.id, "You registered successfuly")
    else:
        await bot.send_message(message.from_user.id, "Your tag no web-site might be wrong. Check it and change is settings!\nIf error persists contact DimoNika.")
        


asyncio.run(bot.polling())