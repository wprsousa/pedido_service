def test_fluxo_completo_pedido(client, pedido_id):
    response = client.get(f"pedidos/{pedido_id}")

    assert response.status_code == 200
    assert response.json()["status"] == "CRIADO"

    response = client.patch(f"pedidos/{pedido_id}/pagar")

    assert response.status_code == 200
    assert response.json()["status"] == "PAGO"

    response = client.patch(f"pedidos/{pedido_id}/enviar")

    assert response.status_code == 200
    assert response.json()["status"] == "ENVIADO"

    response = client.patch(f"pedidos/{pedido_id}/entregar")

    assert response.status_code == 200
    assert response.json()["status"] == "ENTREGUE"


def test_criar_pedido_produto_inexistente(client):
    response = client.get("pedidos/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado: 1"


def test_pagar_pedido_inexistente(client):
    response = client.patch("pedidos/1/pagar")

    assert response.status_code == 404
    assert response.json()["detail"] == "Pedido não encontrado: 1"


def test_transicao_invalida(client, pedido_id):
    response = client.patch(f"pedidos/{pedido_id}/entregar")

    print(response.json())
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Não é possível transitar do status 'CRIADO' para 'ENTREGUE'."
    )


def test_cancelar_pedido(client, pedido_id):
    response = client.patch(f"pedidos/{pedido_id}/entregar")

    print(response.json())
    assert response.status_code == 400
    assert (
        response.json()["detail"]
        == "Não é possível transitar do status 'CRIADO' para 'ENTREGUE'."
    )
