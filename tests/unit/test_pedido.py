import pytest
from datetime import datetime

from src.model.item_pedido import ItemPedido
from src.model.pedido import Pedido
from src.model.status_pedido import StatusPedido
from src.model.exceptions import PedidoNaoEncontradoException, TransicaoInvalidaException


def criar_pedido() -> Pedido:
    itens = [
        ItemPedido(produto_id="1", nome_produto="Macbook", quantidade=1, preco_unitario=7999.0),
        ItemPedido(produto_id="2", nome_produto="MagicMouse", quantidade=2, preco_unitario=599.0),
    ]
    return Pedido(cliente="Wellington Pedro", itens=itens)


def test_pedido_criado_com_status_criado():
    pedido = criar_pedido()
    assert pedido.status == StatusPedido.CRIADO


def test_calcular_valor_total():
    pedido = criar_pedido()
    assert pedido.valor_total == 9197


def test_pagar_pedido():
    pedido = criar_pedido()
    pedido.pagar()
    assert pedido.status == StatusPedido.PAGO


def test_pagar_pedido_ja_pago():
    pedido = criar_pedido()
    pedido.pagar()
    with pytest.raises(TransicaoInvalidaException):
        pedido.pagar()


def test_enviar_pedido_pago():
    pedido = criar_pedido()
    pedido.pagar()
    pedido.enviar()
    assert pedido.status == StatusPedido.ENVIADO


def test_cancelar_pedido_criado():
    pedido = criar_pedido()
    pedido.cancelar()
    assert pedido.status == StatusPedido.CANCELADO


def test_fluxo_completo():
    pedido = criar_pedido()
    pedido.pagar()
    pedido.enviar()
    pedido.entregar()
    assert pedido.status == StatusPedido.ENTREGUE
