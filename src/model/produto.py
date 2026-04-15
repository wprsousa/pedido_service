from dataclasses import dataclass


@dataclass
class Produto:
    id: str
    nome: str
    preco: float
    ativo: bool
    quantidade_estoque: int = 0
