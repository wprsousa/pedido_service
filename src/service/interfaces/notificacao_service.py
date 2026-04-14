from abc import ABC, abstractmethod

from src.model.pedido import Pedido


class NotificacaoServiceInterface(ABC):
    @abstractmethod
    def notificar(self, pedido: Pedido) -> None:
        pass
