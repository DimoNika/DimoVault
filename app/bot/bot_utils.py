from telebot.async_telebot import AsyncTeleBot
from telebot.types import InputFile

from dotenv import load_dotenv
import os
load_dotenv()

print(os.getenv("TG_BOT_TOKEN"))
bot = AsyncTeleBot(os.getenv("TG_BOT_TOKEN"))

import pymongo


#  adress from .env
dbclient = pymongo.MongoClient(os.getenv("DB_CONNECTION_STRING"))



db = dbclient["vault_db"]
# items_table = db["items"]
users_table = db["users"]
files_table = db["files"]



# async def file_tg_send():
async def file_tg_send(siteUsername, system_filename):

    user = users_table.find_one({"site_username": siteUsername})
    file = files_table.find_one({"system_filename": system_filename})
    await bot.send_document(user["chat_id"], InputFile(file["filepath"], file["filename"]))
    
    # await bot.close()