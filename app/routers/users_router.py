from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.roles import RoleEnum
from fastapi import APIRouter, Depends, HTTPException
from app.auth.security import require_roles, get_current_user
from app.models import Usuario
from app.schemas import UpdateRoleSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/me")
def read_me(usuario: Usuario = Depends(get_current_user)):
    return {
        "id": usuario.id,
        "username": usuario.username,
        "role": usuario.role
    }

@router.patch("/{user_id}/role")
def alterar_role(
    user_id: int,
    data: UpdateRoleSchema,
    db: Session = Depends(get_db),
    admin: Usuario = Depends(require_roles(RoleEnum.admin))
):
    user = db.query(Usuario).filter(Usuario.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    user.role = data.novo_role.value
    db.commit()

    return {"msg": f"Role de usuário {user.username} atualizado para {data.novo_role.value}"}
