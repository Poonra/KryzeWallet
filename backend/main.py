from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routes import router


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "WELCOME TO KRYZE WALLET API"}
