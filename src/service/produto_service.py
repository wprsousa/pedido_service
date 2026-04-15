import uuid
from logging import getLogger

from src.model.produto import Produto
from src.service.interfaces.produto_repository import ProdutoRepositoryInterface

logger = getLogger(__name__)


class ProdutoService(ProdutoRepositoryInterface):
    def __init__(self, produto_repository: ProdutoRepositoryInterface):
        self.produto_repository = produto_repository

    def criar_produto(self, nome: str, preco: float, quantidade: int) -> Produto:
        logger.info(f"Criando produto: {nome} - {preco} - {quantidade}")
        produto = Produto(
            id=str(uuid.uuid4()),
            nome=nome,
            preco=preco,
            ativo=True,
            quantidade_estoque=quantidade,
        )
        logger.info(f"Produto criado: {produto}")
        self.produto_repository.salvar_produto(produto)
        return produto

    def salvar_produto(self, produto: Produto) -> None:
        self.produto_repository.salvar_produto(produto)

    def buscar_produto_por_id(self, produto_id: str) -> Produto | None:
        return self.produto_repository.buscar_produto_por_id(produto_id)

    def listar_produtos(self) -> list[Produto]:
        return self.produto_repository.listar_produtos()
