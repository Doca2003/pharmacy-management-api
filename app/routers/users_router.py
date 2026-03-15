from fastapi import APIRouter, Depends
from app.auth.security import get_current_user
from app.models import Usuario

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
