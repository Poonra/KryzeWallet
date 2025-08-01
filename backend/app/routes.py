from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.auth import getCurrentUser
from app import schemas, models, database, auth

router = APIRouter()


@router.get("/me")
def getProfile(current_user: dict = Depends(getCurrentUser)):
    return{"user": current_user}