from src.repository.console_notificacao_adapter import ConsoleNotificacaoAdapter
from src.repository.pedido_repository_memory import PedidoRepositoryMemory
from src.repository.produto_repository_memory import ProdutoRepositoryMemory
from src.service.pedido_service import PedidoService
from src.service.produto_service import ProdutoService

_pedido_repo = PedidoRepositoryMemory()
_produto_repo = ProdutoRepositoryMemory()
_notificacao = ConsoleNotificacaoAdapter()


def get_produto_service() -> ProdutoService:
    return ProdutoService(produto_repository=_produto_repo)


def get_pedido_service() -> PedidoService:
    return PedidoService(
        pedido_repository=_pedido_repo,
        produto_repository=_produto_repo,
        notificacao=_notificacao,
    )
