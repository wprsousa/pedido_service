from pydantic import BaseModel

from src.model.produto import Produto


class ProdutoResponse(BaseModel):
    id: str
    nome: str
    preco: float
    ativo: bool
    quantidade_estoque: int = 0

    @classmethod
    def from_model(cls, produto: Produto) -> "ProdutoResponse":
        return cls(
            id=produto.id,
            nome=produto.nome,
            preco=produto.preco,
            ativo=produto.ativo,
            quantidade_estoque=produto.quantidade_estoque,
        )
