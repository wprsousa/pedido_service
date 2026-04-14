from fastapi import APIRouter, Depends, HTTPException, status

from src.config.dependencies import get_pedido_service
from src.controller.dto.pedido_request import PedidoRequest
from src.controller.dto.pedido_response import PedidoResponse
from src.model import exceptions
from src.service.pedido_service import PedidoService

router = APIRouter()


@router.post("/", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
def criar_pedido(
    request: PedidoRequest, service: PedidoService = Depends(get_pedido_service)
) -> PedidoResponse:
    try:
        pedido = service.criar_pedido(
            request.cliente, itens=[item.model_dump() for item in request.itens]
        )
        return PedidoResponse.from_model(pedido)
    except exceptions.ProdutoNaoEncontradoException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{pedido_id}", response_model=PedidoResponse)
def buscar_pedido_por_id(
    pedido_id: str, service: PedidoService = Depends(get_pedido_service)
) -> PedidoResponse:
    try:
        pedido = service.buscar_pedido(pedido_id)
        return PedidoResponse.from_model(pedido)
    except exceptions.PedidoNaoEncontradoException as e:
        raise HTTPException(
            status_code=404, detail=f"Pedido não encontrado: {e.pedido_id}"
        )


@router.patch("/{pedido_id}/pagar", response_model=PedidoResponse)
def pagar_pedido(pedido_id: str, service: PedidoService = Depends(get_pedido_service)) -> PedidoResponse:
    try:
        pedido = service.pagar_pedido(pedido_id)
        return PedidoResponse.from_model(pedido)
    except exceptions.PedidoNaoEncontradoException as e:
        raise HTTPException(
            status_code=404, detail=f"Pedido não encontrado: {e.pedido_id}"
        )
    except exceptions.TransicaoInvalidaException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{pedido_id}/enviar", response_model=PedidoResponse)
def enviar_pedido(pedido_id: str, service: PedidoService = Depends(get_pedido_service)) -> PedidoResponse:
    try:
        pedido = service.enviar_pedido(pedido_id)
        return PedidoResponse.from_model(pedido)
    except exceptions.PedidoNaoEncontradoException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except exceptions.TransicaoInvalidaException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{pedido_id}/entregar", response_model=PedidoResponse)
def entregar_pedido(pedido_id: str, service: PedidoService = Depends(get_pedido_service)) -> PedidoResponse:
    try:
        pedido = service.entregar_pedido(pedido_id)
        return PedidoResponse.from_model(pedido)
    except exceptions.PedidoNaoEncontradoException as e:
        raise HTTPException(
            status_code=404, detail=f"Pedido não encontrado: {e.pedido_id}"
        )
    except exceptions.TransicaoInvalidaException as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.patch("/{pedido_id}/cancelar", response_model=PedidoResponse)
def cancelar_pedido(pedido_id: str, service: PedidoService = Depends(get_pedido_service)) -> PedidoResponse:
    try:
        pedido = service.cancelar_pedido(pedido_id)
        return PedidoResponse.from_model(pedido)
    except exceptions.PedidoNaoEncontradoException as e:
        raise HTTPException(
            status_code=404, detail=f"Pedido não encontrado: {e.pedido_id}"
        )
    except exceptions.TransicaoInvalidaException as e:
        raise HTTPException(status_code=400, detail=str(e))
