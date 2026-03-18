from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Usuario
from app.schemas import Token
from app.auth.security import hash_senha, verificar_senha, criar_token
from app.schemas import UsuarioCreate
from app.auth.roles import RoleEnum


router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

#registrar usuario
@router.post("/register")
def register(usuario: UsuarioCreate, db:Session = Depends(get_db)):
    user_existente = db.query(Usuario).filter(Usuario.username == usuario.username).first()

    if user_existente:
        raise HTTPException(status_code=400, detail="Usuário já existe")
    
    
    senha_hash = hash_senha(usuario.password)
    novo_usuario = Usuario(username=usuario.username, senha_hash=senha_hash, role=RoleEnum.funcionario.value)

    db.add(novo_usuario)
    db.commit()

    return {"msg":"Usuário criado com sucesso"}


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    usuario = db.query(Usuario).filter(
        Usuario.username == form_data.username
    ).first()

    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário inválido")

    if not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(status_code=400, detail="Senha inválida")

    token = criar_token({"sub": usuario.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

