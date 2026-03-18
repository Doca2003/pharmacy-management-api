from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.database import get_db
from app.models import Pedido, ItemPedido, Medicamento, Usuario
from app.schemas import PedidoResponse, ItemPedidoCreate, PaginatedPedidos
from datetime import datetime, timezone
from app.auth.security import require_roles
from app.routers.users_router import RoleEnum


router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

def verificar_pedido_aberto(pedido):
    if pedido.status != "ABERTO":
        raise HTTPException(status_code=400, detail="Pedido já finalizado")

#listar os pedidos(paginacao)
@router.get("/", response_model=PaginatedPedidos)
def listar_pedidos(status: str = Query(None),data_inicio: datetime = Query(None),data_fim: datetime = Query(None),sort_by: str = Query("data"),order: str = Query("desc"), page: int = Query(1, ge=1), limit: int = Query(10, ge=1,le=100), db:Session = Depends(get_db)):
    query = db.query(Pedido)

    if status:
        query = query.filter(Pedido.status == status)

    if data_inicio:
        query = query.filter(Pedido.data_fechamento >= data_inicio)
    
    if data_fim:
        query = query.filter(Pedido.data_fechamento <= data_fim)

    #ordenacao no banco

    if sort_by == "data":
        if order == "desc":
            query = query.order_by(desc(Pedido.data_fechamento))
        else:
            query = query.order_by(asc(Pedido.data_fechamento))
        
        total = query.count()
        offset = (page - 1)*limit
        pedidos = query.offset(offset).limit(limit).all()

    else:
        #ordenacao por valor total python
        pedidos = query.all()

        if sort_by == "valor_total":
            pedidos = sorted(pedidos,key=lambda p: p.valor_total, reverse=(order=="desc"))
        
        total = len(pedidos)

        #paginacao manual
        start = (page-1)*limit
        end = start+limit
        pedidos = pedidos[start:end]

    return{
        "page":page,
        "limit":limit,
        "total":total,
        "data":pedidos
    }

#criar pedido

@router.post("/", response_model=PedidoResponse)
def criar_pedido(db: Session = Depends(get_db), usuario: Usuario = Depends(require_roles(RoleEnum.funcionario))):
    novo_pedido = Pedido(status="ABERTO",data_criacao=datetime.now())
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido


#adicionar item ao pedido
@router.post("/{pedido_id}/itens")
def adicionar_item(
    pedido_id: int,
    item: ItemPedidoCreate,
    db: Session = Depends(get_db),
    usuario: Usuario = Depends(require_roles(RoleEnum.funcionario))
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
    if medicamento.validade < datetime.now(timezone.utc):
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

    return pedido


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
def finalizar_pedido(pedido_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(require_roles(RoleEnum.funcionario, RoleEnum.admin))):

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
    
    
