import pytest

from src.model.exceptions import (
    EstoqueInsuficienteException,
    PedidoNaoEncontradoException,
    ProdutoNaoEncontradoException,
)
from src.model.pedido import Pedido
from src.model.produto import Produto
from src.model.status_pedido import StatusPedido


def test_criar_pedido_com_sucesso(pedido_service):
    service, pedido_repo, produto_repo, notificacao_repo = pedido_service

    produto1 = Produto(
        id="1", nome="Playstation 5", preco=3999.0, ativo=True, quantidade_estoque=3
    )
    produto2 = Produto(
        id="2",
        nome="Red Dead Redemption",
        preco=195.0,
        ativo=True,
        quantidade_estoque=5,
    )

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
    assert produto_repo.salvar_produto.call_count == 2
    produto_repo.salvar_produto.assert_any_call(produto1)
    produto_repo.salvar_produto.assert_any_call(produto2)

    assert produto1.quantidade_estoque == 2
    assert produto2.quantidade_estoque == 3


def test_criar_pedido_com_produto_inexistente(pedido_service):
    service, pedido_repo, produto_repo, notificacao_repo = pedido_service

    produto1 = Produto(
        id="1", nome="Playstation 5", preco=3999.0, ativo=True, quantidade_estoque=3
    )

    def mock_buscar_produto_por_id(produto_id):
        if produto_id == "1":
            return produto1
        return None

    produto_repo.buscar_produto_por_id.side_effect = mock_buscar_produto_por_id

    itens = [{"produto_id": "1", "quantidade": 1}, {"produto_id": "2", "quantidade": 2}]

    with pytest.raises(ProdutoNaoEncontradoException) as exc_info:
        service.criar_pedido("Cliente Teste", itens)

    assert exc_info.value.produto_id == "2"


def test_criar_pedido_com_estoque_insuficiente(pedido_service):
    service, pedido_repo, produto_repo, notificacao_repo = pedido_service

    produto1 = Produto(
        id="1",
        nome="Playstation 5",
        preco=3999.0,
        ativo=True,
        quantidade_estoque=1,  # Apenas 1 em estoque
    )

    def mock_buscar_produto_por_id(produto_id):
        if produto_id == "1":
            return produto1
        return None

    produto_repo.buscar_produto_por_id.side_effect = mock_buscar_produto_por_id

    itens = [{"produto_id": "1", "quantidade": 2}]

    with pytest.raises(EstoqueInsuficienteException) as exc_info:
        service.criar_pedido("Cliente Teste", itens)

    assert exc_info.value.produto_id == "1"
    assert exc_info.value.quantidade_solicitada == 2
    assert exc_info.value.quantidade_disponivel == 1


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
