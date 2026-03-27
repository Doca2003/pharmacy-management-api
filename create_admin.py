
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from dotenv import load_dotenv

load_dotenv()

from app.database import SessionLocal
from app.models import Usuario
from app.auth.security import hash_senha
from app.routers.users_router import RoleEnum


def criar_admin():
    
    # Lê as credenciais do ambiente
    username = os.getenv("ADMIN_USERNAME")
    password = os.getenv("ADMIN_PASSWORD")

    # Verifica se as variáveis estão definidas
    if not username or not password:
        print("ERRO: Variáveis de ambiente ADMIN_USERNAME ou ADMIN_PASSWORD não definidas no .env")
        return

    db = SessionLocal()
    try:
        # Verifica se já existe um administrador
        admin_existente = db.query(Usuario).filter(Usuario.role == RoleEnum.admin).first()
        if admin_existente:
            print(f"Já existe um administrador no sistema (username: {admin_existente.username}). Nenhuma ação necessária.")
            return

        # Cria o hash da senha
        hashed = hash_senha(password)

        # Cria o novo administrador
        admin = Usuario(
            username=username,
            hashed_password=hashed,
            role=RoleEnum.admin
        )
        db.add(admin)
        db.commit()
        print(f"Administrador criado com sucesso!")
        print(f"Username: {username}")
        print("(senha conforme configurada no .env)")
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar administrador: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    criar_admin()
