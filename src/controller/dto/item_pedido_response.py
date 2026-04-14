from pydantic import BaseModel

from src.model.item_pedido import ItemPedido


class ItemPedidoResponse(BaseModel):
    produto_id: str
    nome: str
    quantidade: int
    preco_unitario: float
    subtotal: float

    @classmethod
    def from_model(cls, item: ItemPedido) -> "ItemPedidoResponse":
        return cls(
            produto_id=item.produto_id,
            nome=item.nome_produto,
            quantidade=item.quantidade,
            preco_unitario=item.preco_unitario,
            subtotal=item.subtotal,
        )
