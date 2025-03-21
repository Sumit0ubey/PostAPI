from fastapi import Depends, status, HTTPException # type: ignore
from fastapi.security import OAuth2PasswordBearer # type: ignore
from sqlalchemy.orm import Session # type: ignore
from jose import JWTError, jwt # type: ignore
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv # type: ignore
from os import getenv

from .schema import TokenData
from .database import get_db
from .models import User

load_dotenv()

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")

KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')
EXPIRE = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

SECRET_KEY = KEY
ALGORITHM = ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = EXPIRE

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: int = payload.get("user_id")
        if id is None:
            raise credential_exception
        token_data = TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credential_exception)
    user = db.query(User).filter(User.id == token.id).first()
    return user
