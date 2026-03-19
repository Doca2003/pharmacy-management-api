from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Medicamento, Usuario
from app.schemas import MedicamentoCreate, MedicamentoResponse, AtualizarEstoque, PaginatedMedicamentos
from typing import List
from datetime import datetime, timezone
from app.auth.security import require_roles
from app.auth.roles import RoleEnum
from sqlalchemy import asc, desc


router = APIRouter(
    prefix="/medicamentos",
    tags=["Medicamentos"]
)

@router.post("/", response_model=MedicamentoResponse)
def criar_medicamento(med: MedicamentoCreate, db: Session = Depends(get_db), usuario: Usuario = Depends(require_roles(RoleEnum.admin, RoleEnum.farmaceutico))):
    novo = Medicamento(**med.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=PaginatedMedicamentos)
def listar_medicamentos(
    nome: str = Query(None),
    estoque_min: int = Query(None),
    sort_by: str = Query("nome"),
    order: str = Query("asc"),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Medicamento)

    #filtros

    if nome:
        query = query.filter(Medicamento.nome.ilike(f"%{nome}%"))

    if estoque_min is not None:
        query = query.filter(Medicamento.quantidade >= estoque_min)

    #ordenacao
    if sort_by == "nome":
        coluna = Medicamento.nome
    elif sort_by == "preco":
        coluna = Medicamento.preco
    elif sort_by == "quantidade":
        coluna = Medicamento.quantidade
    else:
        coluna = Medicamento.nome

    if order == "desc":
        query = query.order_by(desc(coluna))
    else:
        query = query.order_by(asc(coluna))

    #pagniacao
    total = query.count()
    offset = (page - 1) * limit
    medicamentos = query.offset(offset).limit(limit).all()

    return {
        "page": page,
        "limit": limit,
        "total": total,
        "data": medicamentos
    }


@router.put("/{med_id}", response_model=MedicamentoResponse)
def atualizar_quantidade(med_id: int,data: AtualizarEstoque, quantidade: int, db: Session = Depends(get_db), usuario: Usuario = Depends(require_roles(RoleEnum.admin,RoleEnum.admin))):

    med.quantidade = data.quantidade
    med = db.query(Medicamento).filter(Medicamento.id == med_id).first()

    if not med:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado no sistema")

    med.quantidade = quantidade

    db.commit()
    db.refresh(med)

    return med


@router.delete("/{med_id}")
def deletar_medicamento(med_id: int, db: Session = Depends(get_db), usuario: Usuario = Depends(require_roles(RoleEnum.admin))):
    med = db.query(Medicamento).filter(Medicamento.id == med_id).first()

    if not med:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado no sistema")

    db.delete(med)
    db.commit()
    return {"msg": "Removido"}

    
@router.get("/vencidos", response_model=List[MedicamentoResponse])
def listar_medicamentos_vencidos(db: Session = Depends(get_db), usuario: Usuario = Depends(require_roles(RoleEnum.admin,RoleEnum.farmaceutico))):

    hoje = datetime.now(timezone.utc)

    medicamentos_vencidos = db.query(Medicamento).filter(
        Medicamento.validade < hoje
    ).all()

    return medicamentos_vencidos

@router.get("/baixo-estoque", response_model=List[MedicamentoResponse])
def medicamentos_baixo_estoque(limite: int = Query(10, description="Limite de estoque mínimo"),db: Session = Depends(get_db)):
    medicamentos = db.query(Medicamento).filter(Medicamento.quantidade < limite).all()

    return medicamentos

