from pydantic import BaseModel, Field


class ItemPedidoRequest(BaseModel):
    produto_id: str
    quantidade: int = Field(..., gt=0)
