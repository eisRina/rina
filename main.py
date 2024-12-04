from fastapi import FastAPI
from pydantic import BaseModel,EmailStr,field_validator,ConfigDict
from database import create_tables, delete_tables
from contextlib import asynccontextmanager
from repository import UserRepository
from schemas import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")

    
app = FastAPI(lifespan=lifespan)

class User(BaseModel):
    username: str
    password: str
    email: EmailStr
    
    @field_validator('password')
    def validatorORG (passphrase):
        if len(passphrase) < 8:
            raise ValueError('Error')
        return (passphrase)
        

'''@app.post("/users")
async def add_user(user: User):
   return {"user":user}'''

@app.get("/")
async def home():
   return {"data": "Hello World"}

class UserEntity(User):
    id: int
    model_config = ConfigDict(from_attributes=True)

@app.get('/users')
async def get_all_users():
    users = await UserRepository.get_users()
    return users

@app.post('/users')
async def add_new_user(user: User):
    await UserRepository.add_user(user)




