from dataclasses import dataclass


@dataclass
class ItemPedido:
    produto_id: str
    nome_produto: str
    quantidade: int
    preco_unitario: float

    @property
    def subtotal(self):
        return self.quantidade * self.preco_unitario
