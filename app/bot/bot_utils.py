from telebot.async_telebot import AsyncTeleBot
from .bot_config import TOKEN
from telebot.types import InputFile

# bot = AsyncTeleBot("7338534439:AAHDCPaKSUEc3eitG4FMgRrSnrRJEWy3E3E")
bot = AsyncTeleBot(TOKEN)

import pymongo



# another adress for developing
# dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
dbclient = pymongo.MongoClient("mongodb://username:shjshcuisai2i2i2@localhost:27017/")



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