from abc import ABC, abstractmethod

from src.model.pedido import Pedido


class PedidoRepositoryInterface(ABC):
    @abstractmethod
    def salvar_pedido(self, pedido: Pedido) -> None:
        pass

    @abstractmethod
    def buscar_pedido_por_id(self, pedido_id: str) -> Pedido | None:
        pass

    @abstractmethod
    def listar_pedido(self) -> list[Pedido]:
        pass
