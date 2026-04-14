from pydantic import BaseModel

from src.controller.dto.item_pedido_request import ItemPedidoRequest


class PedidoRequest(BaseModel):
    cliente: str
    itens: list[ItemPedidoRequest]
