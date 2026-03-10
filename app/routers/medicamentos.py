from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Medicamento
from app.schemas import MedicamentoCreate, MedicamentoResponse

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


@router.get("/", response_model=list[MedicamentoResponse])
def listar_medicamentos(db: Session = Depends(get_db)):
    return db.query(Medicamento).all()


@router.put("/{med_id}")
def atualizar_quantidade(med_id: int, quantidade: int, db: Session = Depends(get_db)):
    med = db.query(Medicamento).filter(Medicamento.id == med_id).first()

    if not med:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado no sistema")

    med.quantidade = quantidade
    db.commit()
    return {"msg": "Atualizado"}


@router.delete("/{med_id}")
def deletar_medicamento(med_id: int, db: Session = Depends(get_db)):
    med = db.query(Medicamento).filter(Medicamento.id == med_id).first()

    if not med:
        raise HTTPException(status_code=404, detail="Medicamento não encontrado no sistema")

    db.delete(med)
    db.commit()
    return {"msg": "Removido"}
