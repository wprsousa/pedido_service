from unittest.mock import Mock

import pytest

from src.model.exceptions import PedidoNaoEncontradoException
from src.model.pedido import Pedido
from src.model.produto import Produto
from src.model.status_pedido import StatusPedido
from src.service.interfaces.notificacao_service import NotificacaoServiceInterface
from src.service.interfaces.pedido_repository import PedidoRepositoryInterface
from src.service.interfaces.produto_repository import ProdutoRepositoryInterface
from src.service.pedido_service import PedidoService


@pytest.fixture
def pedido_service():
    pedido_repo = Mock(spec=PedidoRepositoryInterface)
    produto_repo = Mock(spec=ProdutoRepositoryInterface)
    notificacao_repo = Mock(spec=NotificacaoServiceInterface)
    service = PedidoService(pedido_repo, produto_repo, notificacao_repo)
    return service, pedido_repo, produto_repo, notificacao_repo


def test_criar_pedido_com_sucesso(pedido_service):
    service, pedido_repo, produto_repo, notificacao_repo = pedido_service

    produto1 = Produto(id="1", nome="Playstation 5", preco=3999.0, ativo=True)
    produto2 = Produto(id="2", nome="Red Dead Redemption", preco=195.0, ativo=True)

    def mock_buscar_produto_por_id(produto_id):
        if produto_id == "1":
            return produto1
        elif produto_id == "2":
            return produto2
        return None

    produto_repo.buscar_produto_por_id.side_effect = mock_buscar_produto_por_id

    itens = [{"produto_id": "1", "quantidade": 1}, {"produto_id": "2", "quantidade": 2}]
    pedido = service.criar_pedido("Cliente Teste", itens)

    assert pedido.cliente == "Cliente Teste"
    assert pedido.status == StatusPedido.CRIADO

    assert pedido.itens[0].produto_id == "1"
    assert pedido.itens[0].nome_produto == "Playstation 5"
    assert pedido.itens[0].quantidade == 1
    assert pedido.itens[0].preco_unitario == 3999.0

    assert pedido.itens[1].produto_id == "2"
    assert pedido.itens[1].nome_produto == "Red Dead Redemption"
    assert pedido.itens[1].quantidade == 2
    assert pedido.itens[1].preco_unitario == 195.0

    assert pedido.valor_total == 4389.0

    pedido_repo.salvar_pedido.assert_called_once_with(pedido)


def test_pagar_pedido_com_sucesso(pedido_service):
    service, pedido_repo, produto_repo, notificacao_repo = pedido_service

    pedido_existente = Pedido(cliente="Cliente Teste", itens=[])
    pedido_repo.buscar_pedido_por_id.return_value = pedido_existente

    pedido_pago = service.pagar_pedido("123")

    assert pedido_pago.status == StatusPedido.PAGO
    assert pedido_pago == pedido_existente

    pedido_repo.buscar_pedido_por_id.assert_called_once_with("123")
    pedido_repo.salvar_pedido.assert_called_once_with(pedido_existente)


def test_pagar_pedido_inexistente_falha(pedido_service):
    service, pedido_repo, produto_repo, notificacao_repo = pedido_service
    pedido_repo.buscar_pedido_por_id.return_value = None
    with pytest.raises(PedidoNaoEncontradoException):
        service.pagar_pedido("123")
    pedido_repo.buscar_pedido_por_id.assert_called_once_with("123")


def test_cancelar_pedido_com_sucesso(pedido_service):
    service, pedido_repo, produto_repo, notificacao_repo = pedido_service

    pedido_existente = Pedido(cliente="Cliente Teste", itens=[])
    pedido_repo.buscar_pedido_por_id.return_value = pedido_existente

    pedido_pago = service.pagar_pedido("123")
    pedido_pago.cancelar()

    assert pedido_pago.status == StatusPedido.CANCELADO
    assert pedido_pago == pedido_existente

    pedido_repo.buscar_pedido_por_id.assert_called_once_with("123")
    pedido_repo.salvar_pedido.assert_called_once_with(pedido_existente)


def test_cancelar_pedido_inexistente_falha(pedido_service):
    service, pedido_repo, produto_repo, notificacao_repo = pedido_service
    pedido_repo.buscar_pedido_por_id.return_value = None
    with pytest.raises(PedidoNaoEncontradoException):
        service.cancelar_pedido("123")
    pedido_repo.buscar_pedido_por_id.assert_called_once_with("123")
