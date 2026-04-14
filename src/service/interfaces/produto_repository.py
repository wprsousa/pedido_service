from abc import ABC, abstractmethod

from src.model.produto import Produto


class ProdutoRepositoryInterface(ABC):
    @abstractmethod
    def salvar_produto(self, produto: Produto) -> None:
        pass

    @abstractmethod
    def buscar_produto_por_id(self, produto_id: str) -> Produto | None:
        pass

    @abstractmethod
    def listar_produtos(self) -> list[Produto]:
        pass
