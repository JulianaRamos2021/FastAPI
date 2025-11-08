
```python

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid  # Biblioteca padrão para gerar códigos únicos

# Instancia o aplicativo FastAPI
app = FastAPI(
    title="TechMarket API",
    description="API para realizar transferências financeiras simuladas",
    version="1.0.0"
)

# ============================================================
# Simulação de um banco de dados simples em memória
# ============================================================

contas = {
    "123": {"nome": "Maria", "saldo": 8500.00},
    "456": {"nome": "João", "saldo": 4000.00}
}

# ============================================================
# Modelo de dados (entrada da API)
# ============================================================

class Transferencia(BaseModel):
    origem: str      # ID da conta de origem
    destino: str     # ID da conta de destino
    valor: float     # Valor a ser transferido

# ============================================================
# Rota principal da aplicação – Endpoint de transferência
# ============================================================

@app.post("/transferencia")
def realizar_transferencia(dados: Transferencia):
    """
    Endpoint que realiza uma transferência financeira entre contas.
    Inclui validação de saldo, registro da operação e código único (UUID).
    """

    # Verifica se as contas existem
    if dados.origem not in contas or dados.destino not in contas:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    # Valida saldo suficiente na conta de origem
    if contas[dados.origem]["saldo"] < dados.valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    # Realiza a transferência (simulação)
    contas[dados.origem]["saldo"] -= dados.valor
    contas[dados.destino]["saldo"] += dados.valor

    # Gera código único para a transação
    codigo_transacao = str(uuid.uuid4())

    # Registra a transação (aqui usamos print, mas poderia ser salvo em um JSON ou banco real)
    print(f"Transferência realizada - Código: {codigo_transacao}")

    # Retorna resposta JSON com confirmação e saldo atualizado
    return {
        "mensagem": "Transferência concluída com sucesso!",
        "codigo_transacao": codigo_transacao,
        "saldo_atual": contas[dados.origem]["saldo"]
    }

# ============================================================
# Instruções:
# Execute o servidor com o comando:
#   uvicorn main:app --reload
# Depois acesse:
#   http://127.0.0.1:8000/docs
# ============================================================
