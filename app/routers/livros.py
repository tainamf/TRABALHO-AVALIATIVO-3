from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import Autor, Livro
from app.schemas.livro import LivroCreate, LivroResponse, LivroUpdate

router = APIRouter(prefix="/livros", tags=["Livros"])


def _garantir_autor(db: Session, autor_id: int) -> None:
    """Validação de integridade: o autor informado precisa existir."""
    if not db.get(Autor, autor_id):
        raise HTTPException(
            status_code=404, detail=f"Autor {autor_id} não encontrado"
        )


@router.post("/", response_model=LivroResponse, status_code=status.HTTP_201_CREATED)
def criar_livro(dados: LivroCreate, db: Session = Depends(get_db)):
    _garantir_autor(db, dados.autor_id)
    livro = Livro(**dados.model_dump())
    db.add(livro)
    db.commit()
    db.refresh(livro)
    return livro


@router.get("/", response_model=list[LivroResponse])
def listar_livros(autor_id: int | None = None, db: Session = Depends(get_db)):
    consulta = select(Livro)
    if autor_id is not None:
        consulta = consulta.where(Livro.autor_id == autor_id)
    return db.scalars(consulta).all()


@router.get("/{livro_id}", response_model=LivroResponse)
def buscar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.get(Livro, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@router.put("/{livro_id}", response_model=LivroResponse)
def atualizar_livro(livro_id: int, dados: LivroUpdate, db: Session = Depends(get_db)):
    livro = db.get(Livro, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")

    alteracoes = dados.model_dump(exclude_unset=True)
    if alteracoes.get("autor_id") is not None:
        _garantir_autor(db, alteracoes["autor_id"])

    for campo, valor in alteracoes.items():
        setattr(livro, campo, valor)
    db.commit()
    db.refresh(livro)
    return livro


@router.delete("/{livro_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_livro(livro_id: int, db: Session = Depends(get_db)):
    livro = db.get(Livro, livro_id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    db.delete(livro)
    db.commit()
