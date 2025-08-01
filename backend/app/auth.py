from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, models, database
from fastapi.security import OAuth2PasswordRequestForm

#---------------------------------------------------
SECRET_KEY = "SECRETGEHEIM" #replace later
ALGORITHM = "HS256" 
ACCESS_TOKEN_EXPIRE_MINUTES = 30
#---------------------------------------------------



pwContext = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hashPw(password: str):
    return pwContext.hash(password)

def verifyPw(plainPw, hashedPw):
    return pwContext.verify(plainPw, hashedPw)


#cretae access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#get DB session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close() 

router = APIRouter()

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

#LOGIN

@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Check if user exists
    dbUser = db.query(models.User).filter(models.User.email == user.username).first()
    if not dbUser or not verifyPw(user.password, dbUser.hashPassword):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    token = create_access_token(data={"sub": dbUser.email})
    return {"access_token":token, "token_type": "bearer", "user_id": dbUser.id}

# protected route example
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def getCurrentUser(token: str = Depends(oauth2_scheme), db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception
    
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user