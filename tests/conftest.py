from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from src.main import app
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

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def produto_id(client):
    response = client.post(
        "/produtos/",
        json={"nome": "Playstation 5", "preco": 3999.00, "quantidade": 3},
    )
    data = response.json()
    produto_id = data["id"]

    return produto_id


@pytest.fixture
def pedido_id(client, produto_id):
    response = client.post(
        "/pedidos/",
        json={
            "cliente": "Teste 1",
            "itens": [{"produto_id": produto_id, "quantidade": 1}],
        },
    )

    data = response.json()
    pedido_id = data["id"]

    return pedido_id
