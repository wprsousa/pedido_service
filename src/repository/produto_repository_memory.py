from src.model.produto import Produto
from src.service.interfaces.produto_repository import ProdutoRepositoryInterface


class ProdutoRepositoryMemory(ProdutoRepositoryInterface):
    def __init__(self):
        self._dados: dict[str, Produto] = {}

    def salvar_produto(self, produto: Produto) -> None:
        self._dados[produto.id] = produto

    def buscar_produto_por_id(self, produto_id: str) -> Produto | None:
        return self._dados.get(produto_id)

    def listar_produtos(self) -> list[Produto]:
        return list(self._dados.values())
