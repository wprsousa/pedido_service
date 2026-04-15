import logging

from src.model import exceptions
from src.model.item_pedido import ItemPedido
from src.model.pedido import Pedido
from src.service.interfaces.notificacao_service import NotificacaoServiceInterface
from src.service.interfaces.pedido_repository import PedidoRepositoryInterface
from src.service.interfaces.produto_repository import ProdutoRepositoryInterface

logger = logging.getLogger(__name__)


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
        logger.info(f"Criando pedido para {cliente} com itens: {len(itens)} item(ns)")
        itens_pedido = []
        for item in itens:
            produto_id = item["produto_id"]
            quantidade = item["quantidade"]
            produto = self.produto_repository.buscar_produto_por_id(produto_id)
            if produto is None:
                logger.error(f"Produto não encontrado: {produto_id}")
                raise exceptions.ProdutoNaoEncontradoException(produto_id)
            if produto.quantidade_estoque < quantidade:
                logger.error(
                    f"Estoque insuficiente para produto {produto_id}: solicitado {quantidade}, disponível {produto.quantidade_estoque}"
                )
                raise exceptions.EstoqueInsuficienteException(
                    produto_id, quantidade, produto.quantidade_estoque
                )
            produto.quantidade_estoque -= quantidade
            self.produto_repository.salvar_produto(produto)
            item_pedido = ItemPedido(
                produto_id=produto_id,
                nome_produto=produto.nome,
                quantidade=quantidade,
                preco_unitario=produto.preco,
            )
            itens_pedido.append(item_pedido)
        pedido = Pedido(cliente=cliente, itens=itens_pedido)
        self.pedido_repository.salvar_pedido(pedido)
        logger.info(
            f"Pedido {pedido.id} criado com sucesso - Total: {pedido.valor_total:.2f}"
        )
        return pedido

    def pagar_pedido(self, pedido_id) -> Pedido:
        logger.info(f"Pagando pedido: {pedido_id}")
        pedido = self.pedido_repository.buscar_pedido_por_id(pedido_id)
        if not pedido:
            logger.error(f"Pedido {pedido_id} não encontrado")
            raise exceptions.PedidoNaoEncontradoException(pedido_id)
        try:
            pedido.pagar()
        except exceptions.TransicaoInvalidaException as e:
            logger.error(f"Transação inválida no pedido {pedido_id}: {e}")
            raise

        self.pedido_repository.salvar_pedido(pedido)
        logger.info(
            f"Pedido {pedido.id} pago com sucesso - Total: {pedido.valor_total:.2f}"
        )
        return pedido

    def enviar_pedido(self, pedido_id) -> Pedido:
        logger.info(f"Enviando pedido: {pedido_id}")
        pedido = self.buscar_pedido(pedido_id)
        if not pedido:
            logger.error(f"Pedido {pedido_id} não encontrado")
            raise exceptions.PedidoNaoEncontradoException(pedido_id)
        pedido.enviar()
        logger.info(f"Pedido {pedido.id} enviado com sucesso")
        return pedido

    def entregar_pedido(self, pedido_id) -> Pedido:
        logger.info(f"Entregando pedido: {pedido_id}")
        pedido = self.buscar_pedido(pedido_id)
        pedido.entregar()
        logger.info(f"Pedido {pedido.id} entregue com sucesso")
        self._notificacao.notificar(pedido)
        return pedido

    def cancelar_pedido(self, pedido_id) -> Pedido:
        logger.info(f"Cancelando pedido: {pedido_id}")
        pedido = self.buscar_pedido(pedido_id)
        pedido.cancelar()
        logger.info(f"Pedido {pedido.id} cancelado com sucesso")
        self.pedido_repository.salvar_pedido(pedido)
        return pedido

    def buscar_pedido(self, pedido_id):
        pedido = self.pedido_repository.buscar_pedido_por_id(pedido_id)
        if pedido is None:
            raise exceptions.PedidoNaoEncontradoException(pedido_id)
        return pedido
