# Importar todos os models aqui garante que o Alembic os enxergue
from app.models.autor import Autor
from app.models.livro import Livro

__all__ = ["Autor", "Livro"]
