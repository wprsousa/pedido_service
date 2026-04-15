from pydantic import BaseModel, Field


class ProdutoRequest(BaseModel):
    nome: str
    preco: float = Field(..., gt=0)
    quantidade: int = Field(..., gt=0)
