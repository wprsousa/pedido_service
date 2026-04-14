# 📦 Pedido Service

Microserviço de gerenciamento de pedidos desenvolvido com **Python**, **FastAPI** e **Pydantic**.

## 📋 Sobre o Projeto

O Pedido Service é um microserviço que implementa uma API RESTful para gerenciar pedidos e seus ciclos de vida. Suporta criação, consulta e transição de estados de pedidos (Criado → Pago → Enviado → Entregue/Cancelado).

### ✨ Principais Características

- ✅ **Arquitetura em camadas** (Controller, Service, Repository, Model)
- ✅ **DTOs** (Data Transfer Objects) para validação de entrada/saída
- ✅ **Injeção de dependências** com FastAPI Depends
- ✅ **Tratamento de exceções** personalizado
- ✅ **Máquina de estados** para transições de pedidos
- ✅ **Testes unitários** com pytest e mocks
- ✅ **Enums tipados** para status

---

## 🏗️ Estrutura do Projeto

```
src/
├── config/                      # Configurações e dependências
│   └── dependencies.py
├── controller/                  # Camada de apresentação
│   ├── pedido_router.py
│   └── dto/                     # Data Transfer Objects
│       ├── pedido_request.py
│       ├── pedido_response.py
│       ├── item_pedido_request.py
│       ├── item_pedido_response.py
│       ├── produto_request.py
│       └── produto_response.py
├── model/                       # Modelos de domínio
│   ├── pedido.py
│   ├── item_pedido.py
│   ├── produto.py
│   ├── status_pedido.py
│   └── exceptions.py
├── repository/                  # Camada de persistência
│   └── interfaces/
│       ├── pedido_repository.py
│       └── produto_repository.py
├── service/                     # Lógica de negócio
│   ├── pedido_service.py
│   ├── produto_service.py
│   └── interfaces/
│       └── notificacao_service.py
└── main.py                      # Aplicação FastAPI

tests/
├── unit/                        # Testes unitários
│   ├── test_pedido.py
│   ├── test_pedido_service.py
│   └── test_produto.py
└── integration/                 # Testes de integração
```

---

## 🚀 Iniciando

### Pré-requisitos

- Python 3.13+
- pip (gerenciador de pacotes Python)
- virtualenv (recomendado)

### Instalação

1. **Clone o repositório**:
```bash
cd /Users/wellingtonpedro/Documents/Projetos/pedido-service
```

2. **Crie e ative um ambiente virtual**:
```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# ou
.venv\Scripts\activate  # Windows
```

3. **Instale as dependências**:
```bash
pip install -r requirements.txt
```

---

## 🏃 Rodando a Aplicação

### Iniciar o servidor FastAPI:
```bash
uvicorn src.main:app --port 8001 --reload
```

A API estará disponível em: **http://127.0.0.1:8001**

### 📚 Acessar a documentação interativa:
- **Swagger UI**: http://127.0.0.1:8001/docs
- **ReDoc**: http://127.0.0.1:8001/redoc

---

## 📡 Endpoints

### Pedidos

#### `POST /pedidos/` - Criar Pedido
Cria um novo pedido com status `CRIADO`.

**Request:**
```json
{
  "cliente": "João Silva",
  "itens": [
    {
      "produto_id": "1",
      "quantidade": 2
    },
    {
      "produto_id": "2",
      "quantidade": 1
    }
  ]
}
```

**Response (201):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "cliente": "João Silva",
  "status": "CRIADO",
  "data_criacao": "2026-04-14T13:48:10.123456",
  "total": 4389.0,
  "itens": [
    {
      "produto_id": "1",
      "nome": "Playstation 5",
      "quantidade": 2,
      "preco_unitario": 1999.0,
      "subtotal": 3998.0
    },
    {
      "produto_id": "2",
      "nome": "Red Dead Redemption",
      "quantidade": 1,
      "preco_unitario": 195.0,
      "subtotal": 195.0
    }
  ]
}
```

---

#### `GET /pedidos/{pedido_id}` - Consultar Pedido
Retorna os detalhes de um pedido específico.

**Response (200):**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "cliente": "João Silva",
  "status": "CRIADO",
  "data_criacao": "2026-04-14T13:48:10.123456",
  "total": 4389.0,
  "itens": [...]
}
```

**Erros:**
- `404 Not Found`: Pedido não encontrado

---

#### `PATCH /pedidos/{pedido_id}/pagar` - Pagar Pedido
Transiciona o pedido para status `PAGO`.

**Response (200):** Pedido atualizado com status `PAGO`

**Erros:**
- `404 Not Found`: Pedido não encontrado
- `400 Bad Request`: Transição inválida

---

#### `PATCH /pedidos/{pedido_id}/enviar` - Enviar Pedido
Transiciona o pedido para status `ENVIADO` (requer status `PAGO`).

**Response (200):** Pedido atualizado com status `ENVIADO`

**Erros:**
- `404 Not Found`: Pedido não encontrado
- `400 Bad Request`: Transição inválida

---

#### `PATCH /pedidos/{pedido_id}/entregar` - Entregar Pedido
Transiciona o pedido para status `ENTREGUE` (requer status `ENVIADO`).

**Response (200):** Pedido atualizado com status `ENTREGUE`

**Erros:**
- `404 Not Found`: Pedido não encontrado
- `400 Bad Request`: Transição inválida

---

#### `PATCH /pedidos/{pedido_id}/cancelar` - Cancelar Pedido
Transiciona o pedido para status `CANCELADO` (requer status `CRIADO` ou `PAGO`).

**Response (200):** Pedido atualizado com status `CANCELADO`

**Erros:**
- `404 Not Found`: Pedido não encontrado
- `400 Bad Request`: Transição inválida

---

## 📊 Fluxo de Estados

```
CRIADO ──pagar──> PAGO ──enviar──> ENVIADO ──entregar──> ENTREGUE
  │                  │
  └──cancelar────────┴──> CANCELADO
```

---

## 🧪 Testes

### Executar todos os testes:
```bash
pytest tests/ -v
```

### Executar apenas testes unitários:
```bash
pytest tests/unit/ -v
```

### Executar teste específico:
```bash
pytest tests/unit/test_pedido_service.py::test_criar_pedido_com_sucesso -v
```

### Com cobertura:
```bash
pytest tests/ --cov=src --cov-report=html
```

---

## 🔧 Tecnologias Utilizadas

- **FastAPI** - Framework web moderno e rápido
- **Pydantic** - Validação de dados e serialização
- **pytest** - Framework de testes
- **Python 3.13** - Linguagem de programação

---

## 📝 Exemplo de Uso (cURL)

### Criar um pedido:
```bash
curl -X POST "http://127.0.0.1:8001/pedidos/" \
  -H "Content-Type: application/json" \
  -d '{
    "cliente": "João Silva",
    "itens": [
      {"produto_id": "1", "quantidade": 2}
    ]
  }'
```

### Consultar um pedido:
```bash
curl -X GET "http://127.0.0.1:8001/pedidos/123e4567-e89b-12d3-a456-426614174000"
```

### Pagar um pedido:
```bash
curl -X PATCH "http://127.0.0.1:8001/pedidos/123e4567-e89b-12d3-a456-426614174000/pagar"
```

### Enviar um pedido:
```bash
curl -X PATCH "http://127.0.0.1:8001/pedidos/123e4567-e89b-12d3-a456-426614174000/enviar"
```

---

## 🏛️ Arquitetura

### Padrões Implementados

1. **Service Layer Pattern**: Lógica de negócio centralizada
2. **Repository Pattern**: Abstração de persistência de dados
3. **Dependency Injection**: Através do FastAPI Depends
4. **DTO Pattern**: Separação entre modelos internos e API
5. **State Machine**: Transições de estados controladas

### Fluxo de Requisição

```
Request HTTP
    ↓
Controller (Router)
    ↓
DTO (Validação)
    ↓
Service (Lógica)
    ↓
Repository (Persistência)
    ↓
Model (Domínio)
    ↓
Response DTO
    ↓
HTTP Response
```

---

## 📚 Documentação de Modelos

### `Pedido`
- `id`: str (UUID)
- `cliente`: str
- `itens`: list[ItemPedido]
- `status`: StatusPedido (enum)
- `data_criacao`: datetime
- `valor_total`: float (property)

### `ItemPedido`
- `produto_id`: str
- `nome_produto`: str
- `quantidade`: int
- `preco_unitario`: float
- `subtotal`: float (property)

### `StatusPedido` (Enum)
- `CRIADO`
- `PAGO`
- `ENVIADO`
- `ENTREGUE`
- `CANCELADO`

---

## ⚙️ Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` (opcional):
```env
DEBUG=True
PORT=8001
```

---

## 🤝 Contribuindo

1. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
2. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
3. Push para a branch (`git push origin feature/AmazingFeature`)
4. Abra um Pull Request

---

## 📄 Licença

Este projeto está sob a licença MIT.

---

## 👨‍💻 Autor

**Wellington Pedro**

---

## 📞 Suporte

Para dúvidas ou sugestões, abra uma issue no repositório.

---

**Última atualização**: Abril de 2026

