from src.model import exceptions
from src.model.item_pedido import ItemPedido
from src.model.pedido import Pedido
from src.service.interfaces.notificacao_service import NotificacaoServiceInterface
from src.service.interfaces.pedido_repository import PedidoRepositoryInterface
from src.service.interfaces.produto_repository import ProdutoRepositoryInterface


class PedidoService:
    def __init__(
        self,
        pedido_repository: PedidoRepositoryInterface,
        produto_repository: ProdutoRepositoryInterface,
        notificacao: NotificacaoServiceInterface,
    ):
        self.pedido_repository = pedido_repository
        self.produto_repository = produto_repository
        self._notificacao = notificacao

    def criar_pedido(self, cliente: str, itens: list[dict]) -> Pedido:
        itens_pedido = []
        for item in itens:
            produto_id = item["produto_id"]
            quantidade = item["quantidade"]
            produto = self.produto_repository.buscar_produto_por_id(produto_id)
            if produto is None:
                raise exceptions.ProdutoNaoEncontradoException(produto_id)
            item_pedido = ItemPedido(
                produto_id=produto_id,
                nome_produto=produto.nome,
                quantidade=quantidade,
                preco_unitario=produto.preco,
            )
            itens_pedido.append(item_pedido)
        pedido = Pedido(cliente=cliente, itens=itens_pedido)
        self.pedido_repository.salvar_pedido(pedido)
        return pedido

    def pagar_pedido(self, pedido_id) -> Pedido:
        pedido = self.buscar_pedido(pedido_id)
        pedido.pagar()
        self.pedido_repository.salvar_pedido(pedido)
        return pedido

    def enviar_pedido(self, pedido_id) -> Pedido:
        pedido = self.buscar_pedido(pedido_id)
        pedido.enviar()
        return pedido

    def entregar_pedido(self, pedido_id) -> Pedido:
        pedido = self.buscar_pedido(pedido_id)
        pedido.entregar()
        self._notificacao.notificar(pedido)
        return pedido

    def cancelar_pedido(self, pedido_id) -> Pedido:
        pedido = self.buscar_pedido(pedido_id)
        pedido.cancelar()
        self.pedido_repository.salvar_pedido(pedido)
        return pedido

    def buscar_pedido(self, pedido_id):
        pedido = self.pedido_repository.buscar_pedido_por_id(pedido_id)
        if pedido is None:
            raise exceptions.PedidoNaoEncontradoException(pedido_id)
        return pedido
