from fastapi import FastAPI
from app.routers import medicamentos, pedidos

app = FastAPI()

app.include_router(medicamentos.router)
app.include_router(pedidos.router)
