from sqlalchemy import Column, Integer, String, DateTime, Float, Date
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

class Medicamento(Base):
    __tablename__ = "medicamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    lote=Column(String) #nao Integer pois pode conter caracteres no lote
    validade=Column(Date)
    quantidade=Column(Integer)
    preco=Column(Float)

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True)
    pedido_id = Column(String, default=lambda: str(uuid.uuid4()))
    status = Column(String, default="ABERTO")
    itens = relationship("ItemPedido", back_populates = "pedido")
    data_fechamento = Column(DateTime, nullable=True)

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

