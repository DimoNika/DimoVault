from datetime import datetime, timedelta, timezone
from jose import jwt




SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 72000  # 50 days

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Добавляем срок действия токена
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(expire)
    return token

