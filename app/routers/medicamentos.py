from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Medicamento
from app.schemas import MedicamentoCreate, MedicamentoResponse
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/medicamentos",
    tags=["Medicamentos"]
)

@router.post("/", response_model=MedicamentoResponse)
def criar_medicamento(med: MedicamentoCreate, db: Session = Depends(get_db)):
    novo = Medicamento(**med.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


@router.get("/", response_model=List[MedicamentoResponse])
def listar_medicamentos(db: Session = Depends(get_db)):
    return db.query(Medicamento).all()


@router.put("/{med_id}", response_model=MedicamentoResponse)
def atualizar_quantidade(med_id: int, quantidade: int, db: Session = Depends(get_db)):

    med = db.query(Medicamento).filter(Medicamento.id == med_id).first()

    if not med:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado no sistema")

    med.quantidade = quantidade

    db.commit()
    db.refresh(med)

    return med


@router.delete("/{med_id}")
def deletar_medicamento(med_id: int, db: Session = Depends(get_db)):
    med = db.query(Medicamento).filter(Medicamento.id == med_id).first()

    if not med:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado no sistema")

    db.delete(med)
    db.commit()
    return {"msg": "Removido"}

    
@router.get("/vencidos", response_model=List[MedicamentoResponse])
def listar_medicamentos_vencidos(db: Session = Depends(get_db)):

    hoje = datetime.now()

    medicamentos_vencidos = db.query(Medicamento).filter(
        Medicamento.validade < hoje
    ).all()

    return medicamentos_vencidos
