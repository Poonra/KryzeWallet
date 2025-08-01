from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr #emailvalidator
    password:str

class Userlogin(BaseModel):
    email: EmailStr
    password: str