from pydantic import BaseModel
from typing import Optional, List
from fastapi import Depends, HTTPException
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "inicio da API"}

# estrutura com classe dos dados de usuario
class User(BaseModel):
    id: int
    name: str
    email: str
    
users_db = []

# listar todos os usuarios usando GET
@app.get("/users", response_model=List[User])
async def get_users():
    return users_db

# puxar usuario com ID usando GET, raise para exceção manual caso o usuario não esteja no db
@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

# criar novo usuario com POST
@app.post("/users", response_model=User)
async def create_user(user: User):
    #raise para ver se o usuario ja existe no db
    for u in users_db:
        if u.id == user.id:
            raise HTTPException(status_code=400, detail="Usuário já existe")
    users_db.append(user)
    return user

#atualizar completamente o usuario com PUT e novamente raise caso o usuario n exista
@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: User):
    for idx, user in enumerate(users_db):
        if user.id == user_id:
            users_db[idx] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

#PATCH para att somente parcial do usuario
@app.patch("/users/{user_id}", response_model=User)
async def partial_update_user(user_id: int, user_update: dict):
    for user in users_db:
        if user.id == user_id:
            #dados que podem ser att e raise novamente(to amando usar raise)
            if "nome" in user_update:
                user.name = user_update["name"]
            if "email" in user_update:
                user.email = user_update["email"]
            if "idade" in user_update:
                user.age = user_update["age"]
            return user
    raise HTTPException(status_code=404, detail="Usuário não encontrado")

#DELETE para apagar o usuario
@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    for idx, user in enumerate(users_db):
        if user.id == user_id:
            del users_db[idx]
            return {"message": "Usuário apagado com sucesso"}
    raise HTTPException(status_code=404, detail="Usuário não encontrado")


