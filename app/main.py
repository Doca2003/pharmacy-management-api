from fastapi import FastAPI
from app.routers import medicamentos, pedidos
from app.auth.auth_router import router as auth_router
from app.routers import users_router

from app.database import Base, engine
from app import models

app = FastAPI()

# cria as tabelas
Base.metadata.create_all(bind=engine)

app.include_router(medicamentos.router)
app.include_router(pedidos.router)
app.include_router(auth_router)
app.include_router(users_router.router)
