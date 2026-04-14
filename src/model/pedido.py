from datetime import datetime
from dataclasses import dataclass, field

from src.model import exceptions
from src.model.item_pedido import ItemPedido
from src.model.status_pedido import StatusPedido
from uuid import uuid4


@dataclass
class Pedido:
    cliente: str
    itens: list[ItemPedido]
    id: str = field(default_factory=lambda: str(uuid4()))
    data_criacao: datetime = field(default_factory=datetime.now)
    status: StatusPedido = StatusPedido.CRIADO

    @property
    def valor_total(self):
        return sum(item.subtotal for item in self.itens)

    def pagar(self):
        if self.status != StatusPedido.CRIADO:
            raise exceptions.TransicaoInvalidaException(self.status, StatusPedido.PAGO)
        self.status = StatusPedido.PAGO

    def enviar(self):
        if self.status != StatusPedido.PAGO:
            raise exceptions.TransicaoInvalidaException(self.status, StatusPedido.ENVIADO)
        self.status = StatusPedido.ENVIADO

    def entregar(self):
        if self.status != StatusPedido.ENVIADO:
            raise exceptions.TransicaoInvalidaException(self.status, StatusPedido.ENTREGUE)
        self.status = StatusPedido.ENTREGUE

    def cancelar(self):
        if self.status not in (StatusPedido.CRIADO, StatusPedido.PAGO):
            raise exceptions.TransicaoInvalidaException(self.status, StatusPedido.CANCELADO)
        self.status = StatusPedido.CANCELADO
