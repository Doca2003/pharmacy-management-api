import os
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Usuario
from app.auth.roles import RoleEnum

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES", 60))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_senha(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha, senha_hash):
    return pwd_context.verify(senha, senha_hash)

def criar_token(dados: dict):
    dados_copia = dados.copy()

    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    dados_copia.update({"exp": expire})

    token = jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)

    return token

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username=payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401,detail="Token Inválido")
        
        usuario = db.query(Usuario).filter(Usuario.username == username).first()

        if usuario is None:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        
        return usuario
    
    except JWTError:
        raise HTTPException(status_code=401, detail="Token Inválido")
    
    
def require_roles(*roles):
    def role_checker(usuario: Usuario = Depends(get_current_user)):
        roles_convertidos = [
            r.value if hasattr(r, "value") else r for r in roles
        ]

        if usuario.role not in roles_convertidos:
            raise HTTPException(status_code=403, detail="Permissão insuficiente")

        return usuario

    return role_checker
