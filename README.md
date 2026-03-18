# 🏦 API de Caixa Eletrônico

Projeto simples de uma API de caixa eletrônico desenvolvida com FastAPI, com foco em praticar lógica de programação e desenvolvimento backend em Python.

---

## 🚀 Funcionalidades

- ✅ Ver saldo
- ➕ Realizar depósitos
- ➖ Realizar saques
- 📄 Visualizar extrato (histórico de operações)

---

## 🧠 Tecnologias utilizadas

- Python
- FastAPI
- Uvicorn

---
## 📌 Rotas disponíveis

| Método | Rota         | Descrição                         |
|--------|--------------|----------------------------------|
| GET    | `/`          | Verifica se a API está ativa     |
| GET    | `/saldo`     | Retorna o saldo atual            |
| POST   | `/depositar` | Realiza um depósito              |
| POST   | `/sacar`     | Realiza um saque                 |
| GET    | `/extrato`   | Mostra o histórico               |