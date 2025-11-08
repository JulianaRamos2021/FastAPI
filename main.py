from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid

app = FastAPI()

# Simulando dados de usuários e saldos
contas = {
    "123": {"nome": "Maria", "saldo": 8500.00},
    "456": {"nome": "João", "saldo": 4000.00}
}

# Modelo de dados para requisição
class Transferencia(BaseModel):
    origem: str
    destino: str
    valor: float

@app.post("/transferencia")
def realizar_transferencia(dados: Transferencia):
    if dados.origem not in contas or dados.destino not in contas:
        raise HTTPException(status_code=404, detail="Conta não encontrada")

    if contas[dados.origem]["saldo"] < dados.valor:
        raise HTTPException(status_code=400, detail="Saldo insuficiente")

    # Realiza transferência
    contas[dados.origem]["saldo"] -= dados.valor
    contas[dados.destino]["saldo"] += dados.valor

    # Gera código único da transação
    codigo_transacao = str(uuid.uuid4())

    # Registra transação (simples print para exemplo)
    print(f"Transferência realizada - Código: {codigo_transacao}")

    return {
        "mensagem": "Transferência concluída com sucesso!",
        "codigo_transacao": codigo_transacao,
        "saldo_atual": contas[dados.origem]["saldo"]
    }
