from passlib.context import CryptContext # type: ignore
from datetime import datetime

pwt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str) -> str:
    return pwt_context.hash(password)

def verify(planPassword: str, hashedPassword: str):
    return pwt_context.verify(planPassword, hashedPassword)

def serialize_timestamp(dt: datetime) -> str:
        return dt.strftime("%d-%m-%Y")
