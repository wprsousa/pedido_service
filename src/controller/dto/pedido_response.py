from pydantic import BaseModel

from src.controller.dto.item_pedido_response import ItemPedidoResponse
from src.model.pedido import Pedido


class PedidoResponse(BaseModel):
    id: str
    cliente: str
    status: str
    data_criacao: str
    total: float
    itens: list[ItemPedidoResponse]

    @classmethod
    def from_model(cls, pedido: Pedido) -> "PedidoResponse":
        return cls(
            id=pedido.id,
            cliente=pedido.cliente,
            status=pedido.status.value,
            data_criacao=pedido.data_criacao.isoformat(),
            total=pedido.valor_total,
            itens=[ItemPedidoResponse.from_model(item) for item in pedido.itens],
        )
