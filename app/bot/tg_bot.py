from bot_config import TOKEN

#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import asyncio

from telebot.async_telebot import AsyncTeleBot

bot = AsyncTeleBot(TOKEN)

import pymongo

# dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
dbclient = pymongo.MongoClient("mongodb://username:shjshcuisai2i2i2@localhost:27017/")



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