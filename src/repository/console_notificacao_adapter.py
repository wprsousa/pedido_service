from src.model.pedido import Pedido
from src.service.interfaces.notificacao_service import NotificacaoServiceInterface


class ConsoleNotificacaoAdapter(NotificacaoServiceInterface):
    def notificar(self, pedido: Pedido) -> None:
        print(
            f"[NOTIFICAÇÃO] Pedido {pedido.id} - Cliente: {pedido.cliente} - Status: {pedido.status} - Total: {pedido.valor_total:.2f}"
        )
