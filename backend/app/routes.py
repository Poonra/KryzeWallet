from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app import schemas, models, database

router = APIRouter()

pwContext = CryptContext(schemes=["bcrypt"], deprecated="auto") #password hashing context

def hashPw(password: str):
    return pwContext.hash(password)

def get_db(): #get database session
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()  #close session so stop connection to DB 

#REGISTER ROUTE
@router.post("/register")

def register(user:schemas.UserCreate, db: Session = Depends(get_db)):

    # Check if user already exists
    existingUser = db.query(models.User).filter(models.User.email == user.email).first()
    if existingUser:
        raise HTTPException(status_code = 400, detail= "Email already registered")
    
    #hash Pw
    hashedPw = hashPw(user.password)

    #create new user as an instance of User model
    newUser = models.User(email= user.email,hashPassword= hashedPw)

    #add to DB

    db.add(newUser)
    db.commit()
    db.refresh(newUser)

    return {"message": "User created successfully", "user_id": newUser.id}