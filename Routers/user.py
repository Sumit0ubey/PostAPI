from fastapi import APIRouter, status, Depends, HTTPException # type: ignore
from sqlalchemy.orm import Session # type: ignore
from sqlalchemy import or_ # type: ignore
from typing import List, Optional

from ..schema import createUser, getUser
from ..database import get_db
from ..models import User
from ..utils import hash

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=getUser)
def createUser(user: createUser, db: Session = Depends(get_db)):
    
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_412_PRECONDITION_FAILED, detail="Mis-Match: password and confirm password must be same")
    
    hashedPassword = hash(user.password)
    new_user = {"name": user.name, "email": user.email, "phoneNo": user.phoneNo, "password": hashedPassword}

    db_user = User(**new_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[getUser])
def getUserProfile(name: str = "", username: Optional[str] = "", db: Session = Depends(get_db)):
    user = db.query(User).filter(or_(User.name.contains(name), User.email.contains(username))).all()
    return user

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=getUser)
def getAuserProfile(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    return user
