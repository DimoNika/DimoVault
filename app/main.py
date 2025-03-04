from fastapi import FastAPI, HTTPException, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from typing import Annotated, Union

from passlib.hash import pbkdf2_sha256

from fastapi.responses import RedirectResponse, Response, FileResponse, JSONResponse

from pydantic import BaseModel, model_validator

from src.token_managment import *

from bot.bot_utils import file_tg_send

import os
from uuid import uuid4

import urllib.parse

from pathlib import Path

from src import qr_managment
from fastapi.staticfiles import StaticFiles

import pymongo

from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Создать папку, если её нет

app = FastAPI()

# FOR DEVELOPMENT?
# Подключаем папку со статикой (пусть будет "static")
# app.mount("/static", StaticFiles(directory="src\\static"), name="static")
# app.mount("/static", StaticFiles(directory="src\\icons"), name="static")


#  adress from .env
dbclient = pymongo.MongoClient(os.getenv("DB_CONNECTION_STRING"))



db = dbclient["vault_db"]
# items_table = db["items"]
users_table = db["users"]
files_table = db["files"]
qrs_table = db["qrs"]


# fot linux
# templates = Jinja2Templates("/app/src/templates")

templates = Jinja2Templates("src/templates")

from src.custom_filters.custom_filters import time_to_human_readable, bytes_to_human_readable, content_type_to_icon

custom_filters = {
    "bytes_to_human_readable": bytes_to_human_readable,
    "time_to_human_readable": time_to_human_readable,
    "content_type_to_icon": content_type_to_icon
}
# Добавляем все фильтры в Jinja
templates.env.filters.update(custom_filters)

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

    return templates.TemplateResponse("index.html", {"request": request})






@app.get("/signup")
async def sign_up(request: Request):
    # if request.query_params.get("error") == None:
    token = request.cookies.get("access_token")
    
    if auth(token):
        return RedirectResponse(f"/vault", status_code=302)
    
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
        users_table.insert_one({"site_username": user_data.siteUsername, "tg_username": user_data.telegramUsername.lower(), "password": pbkdf2_sha256.hash(user_data.pass1)} )
    else:
        return RedirectResponse(f"/signup?error=Username already taken.", status_code=302)
    # x = users_table.find_one({"site_username": user_data.siteUsername})
    x = users_table.find_one({"site_username": "a"})
    print(x)


    # form_data = await request.form()
    # print(form_data)# Создаем RedirectResponse
    redirect_response = RedirectResponse(url="/vault", status_code=302)

    token = create_access_token({"siteUsername": user_data.siteUsername})
    # Добавляем Set-Cookie в ответ
    redirect_response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=4_320_000,
        samesite="Strict",
        secure=True
    )
    return redirect_response



@app.get("/login")
async def login(request: Request):
    # if request.query_params.get("error") == None:
    token = request.cookies.get("access_token")
    
    if auth(token):
        return RedirectResponse(f"/vault", status_code=302)
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

    # return user_instance["password"]
    if user:
        if pbkdf2_sha256.verify(user_data.password, user["password"]):
            token = create_access_token({"siteUsername": user_data.siteUsername})

            # Создаем RedirectResponse
            redirect_response = RedirectResponse(url="/vault", status_code=302)

            # Добавляем Set-Cookie в ответ
            redirect_response.set_cookie(
                key="access_token",
                value=token,
                httponly=True,
                max_age=4_320_000,
                samesite="Strict",
                secure=True
            )

        return redirect_response
    return RedirectResponse(f"/login?error=Wrong credentials.", status_code=302)

@app.get("/vault")
async def vault(request: Request):
    token = request.cookies.get("access_token")
    print(auth(token))
    if auth(token):    
        owner = extract(token)["siteUsername"]
        data = files_table.find({"owner": owner}).sort("upload_date", -1)

        # Chech if user has tg conncted
        if users_table.find_one({"site_username": owner}).get("chat_id"):
            is_tg_connected = True
        else:
            is_tg_connected = False
        return templates.TemplateResponse("vault.html", {"request": request, "files": [x for x in data], "is_tg_connected": is_tg_connected})
    else:
        return RedirectResponse(f"/login", status_code=302)

        # return "User not authenticated"


@app.post("/upload")
async def upload(request: Request, file: UploadFile = File(), tg_send: bool = Form(False)):
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
            # "upload_date": datetime.now().strftime("%H:%M %d.%m.%Y"),
            "upload_date": datetime.now(timezone.utc) + timedelta(hours=2),
            "owner": extract(token)["siteUsername"]
        }

        files_table.insert_one(file_data)
        # print(extract(token)["siteUsername"])
        # print(extract(token))

        # print(file_data)
        if tg_send != False:
            # Check if file less then 50 MB
            if file.size < 52428800:
                siteUsername = extract(token)["siteUsername"]

                if users_table.find_one({"site_username": siteUsername}).get("chat_id"):
                    await file_tg_send(siteUsername, system_filename)
            else:
                pass
            
        return RedirectResponse(f"/vault", status_code=302)
        
    else: 
        return "User not authnticated"
    

@app.get("/download/{filename}")
async def download_file(filename: str):
    print(filename)
    file = files_table.find_one({"filename": filename})
    # file_path = file["filepath"]
    if file:
        return FileResponse(file["filepath"], media_type="application/octet-stream", filename=file["filename"])
    return {"error": "Файл не найден"}

@app.get("/view/{filename}")
async def view_file(filename: str):
    print(filename)
    # filename = urllib.parse.unquote(filename)  # Декодируем %20 в пробелы
    file = files_table.find_one({"filename": filename})
    
    if file:
        encoded_filename = urllib.parse.quote(file["filename"])
        return FileResponse(
            file["filepath"],
            media_type=file["content_type"],  # Укажи нужный MIME-тип
            # headers={"Content-Disposition": f"inline; filename={file["filename"]}"}
            headers={
                "Content-Disposition": f"inline; filename*=UTF-8''{encoded_filename}"
            }

        )
    return {"error": "Файл не найден"}


@app.get("/settings")
async def settings(request: Request):
    token = request.cookies.get("access_token")
    
    
    if auth(token):
        siteUsername = extract(token)["siteUsername"]
        print(siteUsername)

        user = users_table.find_one({"site_username": siteUsername})

        success = request.query_params.get("success")
        error = request.query_params.get("error")


        return templates.TemplateResponse("settings.html", {"request": request, "user": user, "success": success,"error": error})
    else:
        return RedirectResponse(f"/signup", status_code=302)

@app.post("/changepass")
async def changepass(request: Request, oldPass: str = Form(), newPass1: str = Form(), newPass2: str = Form()):
    # return f"{oldPass}{newPass1}{newPass2}{type(newPass2)}"
    token = request.cookies.get("access_token")
    if auth(token):
        site_username = extract(token)["siteUsername"]
        user = users_table.find_one({"site_username": site_username})
        if pbkdf2_sha256.verify(oldPass, user["password"]):
            if newPass1 == newPass2:
                if len(newPass1) >= 6 and len(newPass1) <= 24:
                    # users_table.update_one({"tg_username": message.from_user.username.lower()}, {"$set": {"chat_id": message.from_user.id}})
                    users_table.update_one({"site_username": site_username}, {"$set": {"password": pbkdf2_sha256.hash(newPass1)}})
                    
                    return RedirectResponse(f"/settings?success=Password changed successfuly.", status_code=302)
                
                else:
                    return RedirectResponse(f"/settings?error=New password too long or too short.", status_code=302)
               
            else:
                return RedirectResponse(f"/settings?error=Passwords don't match.", status_code=302)
        else: 
            return RedirectResponse(f"/settings?error=Wrong password.", status_code=302)
           
        
    return RedirectResponse(f"/", status_code=302)
     
@app.post("/deletefiles")
async def deletefiles(request: Request):
    token = request.cookies.get("access_token")

    if auth(token):
        siteUsername = extract(token)["siteUsername"]
        
        files_pathes = [x["filepath"] for x in files_table.find({"owner": siteUsername})]
        print(files_pathes)
        for file in files_pathes:
            path = Path(file)
            try:
                path.unlink()
                
            except FileNotFoundError:
                print(f"{file} not found")
            except Exception as e:
                print(f"Ошибка при удалении {file}: {e}")
        

        files_table.delete_many({"owner": siteUsername})
        return RedirectResponse(f"/vault", status_code=302)
        
    return RedirectResponse(f"/", status_code=302)


@app.post("/changetg")
async def changetg(request: Request, tg_tag: str = Form()):
    token = request.cookies.get("access_token")

    if auth(token):
        siteUsername = extract(token).get("siteUsername")
        # siteUsername = extract(token)
        # return siteUsername
        # print(users_table.find_one({"site_username": siteUsername}))
        users_table.update_one({"site_username": siteUsername}, {"$set": {"tg_username": tg_tag.lower(), "chat_id": None}})
        return RedirectResponse(f"/settings", status_code=302)
        
    return RedirectResponse(f"/", status_code=302)    


@app.get("/logout")
async def logout(request: Request, response: Response):

    redirect_response = RedirectResponse(url="/", status_code=302)

    # Добавляем Set-Cookie в ответ
    redirect_response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        max_age=4_320_000,
        samesite="Strict",
        secure=True
    )
    return redirect_response

@app.get("/qr")
async def qr(request: Request):
    token = request.cookies.get("access_token")

    if auth(token):
        return RedirectResponse(f"/vault", status_code=302)

    qr_code_name = qr_managment.generate_qr()

    return templates.TemplateResponse("qr.html", {"request": request, "qr_code_name": qr_code_name})

@app.get("/scan")
async def scan(request: Request):
    token = request.cookies.get("access_token")

    if auth(token):


        return templates.TemplateResponse("scan.html", {"request": request})
    else:
        return RedirectResponse(f"/", status_code=302)


@app.post("/is-scanned")
async def is_scanned(request: Request):
    
    data = await request.json()
    qr_name = data["qr_code_name"]
    qr_code = qrs_table.find_one({"qr_name": qr_name})
    if qr_code["is_scanned"]:

        token = create_access_token({"siteUsername": qr_code["scanned_by"]})
        # Создаем RedirectResponse
        redirect_response = RedirectResponse(url="/vault", status_code=302)

        # Добавляем Set-Cookie в ответ
        redirect_response.set_cookie(
            key="access_token",
            value=token,
            httponly=True,
            max_age=4_320_000,
            samesite="Strict",
            secure=True
        )

        return redirect_response
        # return qrs_table.find_one({"qr_name": qr_name}).get("scanned_by")
    else:
        return "QR not scanned"

    return data 





@app.post("/qr-validate")
async def qr_validate(request: Request):
    token = request.cookies.get("access_token")
    
    
    if auth(token):
        data = await request.json()
        if not data and not data["qr_data"]: raise HTTPException(status_code=400, detail="No data passed")

        qr_code = qrs_table.find_one({"qr_data": data["qr_data"]})
        # print(qr_code)
        if not qr_code: raise HTTPException(status_code=400, detail="Invalid data passed")

        now = datetime.now(timezone.utc)
        
        # add zone awareness 
        qr_code_created_at = qr_code["created_at"].replace(tzinfo=timezone.utc)
        if (now - qr_code_created_at) > timedelta(minutes=1):
            raise HTTPException(status_code=400, detail="QR code expired")
        
        if qr_code["is_scanned"] == True:
            raise HTTPException(status_code=400, detail="QR alredy used")
        # print(extract(token).get("siteUsername"))
        qrs_table.update_one(qr_code, {"$set": {"is_scanned": True, "scanned_by": extract(token).get("siteUsername")}})

        return JSONResponse(content={"data": "QR code identified"}, status_code = 200)

    else:

        return RedirectResponse(f"/", status_code=302)
    