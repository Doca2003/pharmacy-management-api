from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Pedido, ItemPedido, Medicamento
from app.schemas import PedidoResponse, ItemPedidoCreate
from datetime import datetime
from typing import List, Optional

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

def verificar_pedido_aberto(pedido):
    if pedido.status != "ABERTO":
        raise HTTPException(status_code=400, detail="Pedido já finalizado")

#listar os pedidos
@router.get("/", response_model=List[PedidoResponse])
def listar_pedidos(
    status: Optional[str] = None,
    db: Session = Depends(get_db)
):

    query = db.query(Pedido)

    if status:
        query = query.filter(Pedido.status == status)

    pedidos = query.all()

    return pedidos

#criar pedido

@router.post("/", response_model=PedidoResponse)
def criar_pedido(db: Session = Depends(get_db)):
    novo_pedido = Pedido()
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido


#adicionar item ao pedido
@router.post("/{pedido_id}/itens")
def adicionar_item(
    pedido_id: int,
    item: ItemPedidoCreate,
    db: Session = Depends(get_db)
):

    #verificar se o pedido existe
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado no sistema")
    verificar_pedido_aberto(pedido)

    #verificar se o medicamento existe
    medicamento = db.query(Medicamento).filter(Medicamento.id == item.medicamento_id).first()
    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado no sistema")

    #verificar estoque
    if medicamento.quantidade < item.quantidade:
        raise HTTPException(status_code=400, detail="Estoque insuficiente")
    
    

    #verificar validade
    if medicamento.validade < datetime.now():
        raise HTTPException(status_code=400, detail="Medicamento vencido não pode ser adicionado ao pedido")

    
    #criar item do pedido
    novo_item = ItemPedido(
        pedido_id=pedido.id,
        medicamento_id=item.medicamento_id,
        quantidade=item.quantidade,
        preco_unitario=medicamento.preco
    )

    #baixar estoque automaticamente
    medicamento.quantidade -= item.quantidade

    db.add(novo_item)
    db.add(medicamento)
    db.commit()
    db.refresh(novo_item)

    return novo_item


#obter pedido com itens
@router.get("/{pedido_id}", response_model=PedidoResponse)
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    return pedido


#deletar item do pedido

@router.delete("/{pedido_id}/itens/{item_id}")
def remover_item_pedido(pedido_id:int, item_id:int, db:Session = Depends(get_db)):

    #verificar se pedido existe
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    verificar_pedido_aberto(pedido)

    #verificacao do item no pedido
    item = db.query(ItemPedido).filter(
        ItemPedido.id == item_id,
        ItemPedido.pedido_id == pedido_id
    ).first()




    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")
    
    #buscar medicamento

    medicamento = db.query(Medicamento).filter(Medicamento.id == item.medicamento_id).first()

    if not medicamento:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado")
    
    
    #devolve ao estoque

    medicamento.quantidade += item.quantidade

    #remover item

    db.delete(item)
    db.commit()
    return{"mensagem":"Item removido do carrinho e estoque atualizado"}

@router.post("/{pedido_id}/finalizar")
def finalizar_pedido(pedido_id: int, db: Session = Depends(get_db)):

    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")

    #verificar se já está finalizado
    if pedido.status != "ABERTO":
        raise HTTPException(status_code=400, detail="Pedido já finalizado")

    #verificar se o pedido tem itens
    if not pedido.itens:
        raise HTTPException(status_code=400, detail="Pedido não possui itens")

    #finalizar pedido
    pedido.status = "FINALIZADO"
    pedido.data_fechamento = datetime.now()

    db.commit()

    return {"mensagem": "Pedido finalizado com sucesso"}
    
    
