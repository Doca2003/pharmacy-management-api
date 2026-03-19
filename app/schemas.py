from pydantic import BaseModel
from typing import List, Optional
from app.auth.roles import RoleEnum
from datetime import datetime

# MEDICAMENTOS

class MedicamentoCreate(BaseModel):
    nome: str
    descricao: Optional[str] = None
    quantidade: int
    lote: str
    preco: float
    validade: datetime


class MedicamentoResponse(BaseModel):
    id: int
    nome: str
    quantidade: int
    preco: float
    validade:datetime

    class Config:
        from_attributes = True


class AtualizarEstoque(BaseModel):
    quantidade: int


class PaginatedMedicamentos(BaseModel):
    page: int
    limit: int
    total: int
    data: List[MedicamentoResponse]



# ITENS DO PEDIDO

class ItemPedidoCreate(BaseModel):
    medicamento_id: int
    quantidade: int


class ItemPedidoResponse(BaseModel):
    id: int
    medicamento_id: int
    quantidade: int
    preco_unitario: float

    class Config:
        from_attributes = True



# PEDIDOS

class PedidoCreate(BaseModel):
    pass


class PedidoResponse(BaseModel):
    id: int
    pedido_id: str
    status: str
    valor_total: float  #funciona com @property
    created_at: datetime
    itens: List[ItemPedidoResponse] = []

    class Config:
        from_attributes = True

class PaginatedPedidos(BaseModel):
    page: int
    limit: int
    total: int
    data: List[PedidoResponse]



# USUÁRIOS / AUTH

class UsuarioCreate(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UpdateRoleSchema(BaseModel):
    novo_role: RoleEnum
