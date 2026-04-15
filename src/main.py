from fastapi import FastAPI

from src.config.logging_config import setup_logging
from src.controller.pedido_router import router as pedido_router
from src.controller.produto_router import router as produto_router

setup_logging()
app = FastAPI(title="Pedido Service", version="1.0.0")

app.include_router(pedido_router, prefix="/pedidos", tags=["pedidos"])
app.include_router(produto_router, prefix="/produtos", tags=["produtos"])
