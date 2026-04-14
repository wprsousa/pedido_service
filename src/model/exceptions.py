from src.model.status_pedido import StatusPedido


class PedidoNaoEncontradoException(Exception):
    def __init__(self, pedido_id: str):
        self.pedido_id = pedido_id
        super().__init__(f"Pedido com ID '{pedido_id}' não foi encontrado.")


class ProdutoNaoEncontradoException(Exception):
    def __init__(self, produto_id: str):
        self.produto_id = produto_id
        super().__init__(f"Produto com ID '{produto_id}' não foi encontrado.")


class TransicaoInvalidaException(Exception):
    def __init__(self, status_atual: StatusPedido, status_destino: StatusPedido):
        self.status_atual = status_atual
        self.status_destino = status_destino
        super().__init__(f"Não é possível transitar do status '{status_atual}' para '{status_destino}'.")
