from sqlalchemy import Column, Integer, String, DateTime, Float, Date, func
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
import uuid

class Medicamento(Base):
    __tablename__ = "medicamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    lote=Column(String) #nao Integer pois pode conter caracteres no lote
    validade=Column(DateTime, nullable=False)
    quantidade=Column(Integer)
    preco=Column(Float)
    descricao = Column(String, nullable=True)

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(String, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="ABERTO")
    itens = relationship("ItemPedido", back_populates = "pedido")
    data_fechamento = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    @property
    def valor_total(self):
        return sum(item.preco_unitario * item.quantidade for item in self.itens)

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"))
    medicamento_id = Column(Integer, ForeignKey("medicamentos.id"))

    quantidade = Column(Integer)
    preco_unitario = Column(Float)

    pedido = relationship("Pedido", back_populates="itens")
    medicamento=relationship("Medicamento")

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    senha_hash = Column(String)
    role = Column(String, default="funcionario")
