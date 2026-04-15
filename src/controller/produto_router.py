from fastapi import APIRouter, Depends, HTTPException, status

from src.config.dependencies import get_produto_service
from src.controller.dto.produto_request import ProdutoRequest
from src.controller.dto.produto_response import ProdutoResponse
from src.service.produto_service import ProdutoService

router = APIRouter()


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(
    request: ProdutoRequest, service: ProdutoService = Depends(get_produto_service)
):
    produto = service.criar_produto(
        nome=request.nome, preco=request.preco, quantidade=request.quantidade
    )
    return ProdutoResponse.from_model(produto)


@router.get("/", response_model=list[ProdutoResponse])
def listar_produtos(service: ProdutoService = Depends(get_produto_service)):
    produtos = service.listar_produtos()
    return [ProdutoResponse.from_model(produto) for produto in produtos]


@router.get("/{produto_id}", response_model=ProdutoResponse)
def consultar_produtos(
    produto_id: str, service: ProdutoService = Depends(get_produto_service)
):
    produto = service.buscar_produto_por_id(produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado.")
    return ProdutoResponse.from_model(produto)
