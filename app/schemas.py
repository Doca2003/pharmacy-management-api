from pydantic import BaseModel
from typing import List, Optional

#MEDICAMENTOS

class MedicamentoCreate(BaseModel):
    nome: str
    quantidade:int
    preco:float

class MedicamentoResponse(BaseModel):
    id:int
    nome:str
    quantidade:int
    preco:float

    class Config:
        orm_mode=True


#ITENS

class ItemPedidoCreate(BaseModel):
    medicamento_id:int
    quantidade: int

class ItemPedidoResponse(BaseModel):
    id: int
    medicamento_id: int
    quantidade: int
    preco_unitario: float

    class Config:
        orm_mode = True
        
#PEDIDOS

class PedidoCreate(BaseModel):
    pass #nao envia nada ainda

class PedidoResponse(BaseModel):
    id: int
    pedido_id: str
    status: str
    valor_total: float
    itens: List[ItemPedidoResponse] = []

    class Config:
        orm_mode = True
