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



# async def file_tg_send():
async def file_tg_send(siteUsername, file_location):

    user = users_table.find_one({"site_username": siteUsername})
    
    await bot.send_document(user["chat_id"], InputFile(f"./{file_location}"))
    
    # await bot.close()