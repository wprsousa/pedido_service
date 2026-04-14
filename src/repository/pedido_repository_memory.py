from src.model.pedido import Pedido
from src.service.interfaces.pedido_repository import PedidoRepositoryInterface


class PedidoRepositoryMemory(PedidoRepositoryInterface):
    def __init__(self):
        self._dados: dict[str, Pedido] = {}

    def salvar_pedido(self, pedido: Pedido) -> None:
        self._dados[pedido.id] = pedido

    def buscar_pedido_por_id(self, pedido_id: str) -> Pedido | None:
        return self._dados.get(pedido_id)

    def listar_pedido(self) -> list[Pedido]:
        return list(self._dados.values())
