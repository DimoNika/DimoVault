from fastapi import FastAPI, HTTPException, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from typing import Annotated, Union

from passlib.hash import pbkdf2_sha256

from fastapi.responses import RedirectResponse, Response

from pydantic import BaseModel, model_validator

from src.token_managment import *

import os
from uuid import uuid4

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Создать папку, если её нет

app = FastAPI()

import pymongo



# another adress for developing
dbclient = pymongo.MongoClient("mongodb://localhost:27017/")
# dbclient = pymongo.MongoClient("mongodb://username:password@mongo:27017/")


db = dbclient["vault_db"]
# items_table = db["items"]
users_table = db["users"]
files_table = db["files"]


# fot linux
# templates = Jinja2Templates("/app/src/templates")

templates = Jinja2Templates("src/templates")

from src.bytes_to_human_readable import bytes_to_human_readable

templates.env.filters['bytes_to_human_readable'] = bytes_to_human_readable


class UserForm(BaseModel):
    siteUsername: str  # Проверка на минимальную длину 6 символов
    telegramUsername: str
    pass1: str
    pass2: str

class UserLogin(BaseModel):
    siteUsername: str
    password: str



def auth(token):
    try:
    # Декодирование токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": True})
        if users_table.find_one({"site_username": payload["siteUsername"]}):

            return True
        else:
            return False
    except Exception as e:
        print("Ошибка декодирования:", str(e))

        return False

def extract(token):
    try:
    # Декодирование токена
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_signature": True})
        

        return payload
    except Exception as e:
        
        return None


@app.get("/")
async def main(request: Request):

    return templates.TemplateResponse("vault.html", {"request": request})



@app.get("/test")
async def main(request: Request):
    # return "hello"
    token = request.cookies.get("access_token")
    
    # Check if user authenticated
    if auth(token):
        payload = extract(token)
    print(payload)
    return payload


@app.get("/signup")
async def sign_up(request: Request):
    # if request.query_params.get("error") == None:
    error = request.query_params.get("error")
    print(error)
    return templates.TemplateResponse("sign_up.html", {"request": request, "error": error})

@app.post("/signup")
async def sign_up(
                    request: Request,
                    siteUsername: Annotated[str, Form()],
                    telegramUsername: Annotated[str, Form()],
                    pass1: Annotated[str, Form()],
                    pass2: Annotated[str, Form()],
                ):
        # Преобразуем данные в Pydantic модель для валидации
    try:
        user_data = UserForm(
            siteUsername=siteUsername,
            telegramUsername=telegramUsername,
            pass1=pass1,
            pass2=pass2
        )
    except BaseException as e:
        print(e)
        return RedirectResponse(f"/signup?error={e}. Something went wrong.", status_code=302)

    if len(user_data.siteUsername) < 4 or len(user_data.siteUsername) > 21:
        return RedirectResponse(f"/signup?error=Username is too short or too long.", status_code=302)
    
    if user_data.pass1 != user_data.pass2:
        return RedirectResponse(f"/signup?error=Passwords dont match.", status_code=302)
    
    if len(user_data.pass1) < 6 or len(user_data.pass1) > 25:
        return RedirectResponse(f"/signup?error=Password too short. 6-24 symbols.", status_code=302)
    
    # User creation
    if not users_table.find_one({"site_username": user_data.siteUsername}):
        users_table.insert_one({"site_username": user_data.siteUsername, "tg_username": user_data.telegramUsername, "password": pbkdf2_sha256.hash(user_data.pass1)} )
    else:
        return RedirectResponse(f"/signup?error=Username already taken.", status_code=302)
    # x = users_table.find_one({"site_username": user_data.siteUsername})
    x = users_table.find_one({"site_username": "a"})
    print(x)


    # form_data = await request.form()
    # print(form_data)
    return dict(user_data)


@app.get("/login")
async def login(request: Request):
    # if request.query_params.get("error") == None:
    error = request.query_params.get("error")
    print(error)
    return templates.TemplateResponse("login.html", {"request": request, "error": error})

@app.post("/login")
async def login(
                    request: Request,
                    siteUsername: Annotated[str, Form()],
                    password: Annotated[str, Form()],
                    response: Response        
                ):
        # Преобразуем данные в Pydantic модель для валидации
    try:
        user_data = UserLogin(
            siteUsername=siteUsername,
            password=password,
        )
    except BaseException as e:
        print(e)

    user = users_table.find_one({"site_username": user_data.siteUsername})
    print(user_data.siteUsername)
    print(user_data.password)
    print(user)

    # return user_instance["password"]
    if user:
        if pbkdf2_sha256.verify(user_data.password, user["password"]):
            token = create_access_token({"siteUsername": user_data.siteUsername})
            response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,      # Доступ только через HTTP (JavaScript не может прочитать куки)
                max_age=4_320_000,    # 50 days. Время жизни токена (в секундах)
                # expires=1800,       # Альтернативный способ указания времени жизни
                samesite="Strict",  # Политика SameSite (например, Strict или Lax)
                secure=True         # Требовать HTTPS (для локальной разработки можно отключить)
            )
            return "Success"
    
    return RedirectResponse(f"/login?error=Wrong credentials.", status_code=302)

@app.get("/vault")
async def vault(request: Request):
    token = request.cookies.get("access_token")

    if auth(token):
        owner = extract(token)["siteUsername"]
        data = files_table.find({"owner": owner})
        return templates.TemplateResponse("vault.html", {"request": request, "files": [x for x in data]})
    else:
        return "User not authenticated"


@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(), tg_send: Union[str, bool] = Form(False)):
    token = request.cookies.get("access_token")
    print(file)
    
    if auth(token):
        
        if file.size == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty.")
        
        # file_location = os.path.join(UPLOAD_DIR, file.filename)
        
        
        system_filename = str(uuid4()) + str(file.filename)

        file_location = os.path.join(UPLOAD_DIR, system_filename)
            
        with open(file_location, "wb") as buffer:
            while chunk := await file.read(1024 * 1024):  # Читаем по 1MB
                buffer.write(chunk)

        file_data = {
            "filename": file.filename,
            "system_filename": system_filename,
            "filepath": file_location,
            "content_type": file.content_type,
            "size": file.size,
            "upload_date": datetime.now().strftime("%H:%M %d.%m.%Y"),
            "owner": extract(token)["siteUsername"]
        }

        files_table.insert_one(file_data)
        # print(extract(token)["siteUsername"])
        # print(extract(token))

        print(file_data)

        # print(await request.form())
        # # print(request.)

        # print(file)
        # print(tg_send)
        return RedirectResponse(f"/vault", status_code=302)
        
    else: 
        return "User not authnticated"
    