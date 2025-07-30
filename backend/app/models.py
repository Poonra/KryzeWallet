from sqlalchemy import Column, Integer, String #import type of columns in DB

from sqlalchemy.orm import declarative_base
Base = declarative_base() # create a base class for all models to inherit from

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key= True,index= True)
    email = Column(String, unique=True, index=True)
    hashPassword = Column(String)