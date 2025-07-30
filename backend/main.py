from fastapi import FastAPI
from app.database import engine
from app.models import Base

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.get("/")
def read_root():
    return {"message": "WELCOME TO KRYZE WALLET API"}
