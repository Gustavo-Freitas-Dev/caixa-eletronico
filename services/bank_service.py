from database.models import carregar_dados, salvar_dados
from datetime import datetime

def depositar(id, valor):
    dados = carregar_dados()

    for u in dados['usuarios']:
        if u['id'] == id:
            u['saldo'] += valor
            u['historico'].append({
                "tipo": "deposito",
                "valor": valor,
                "data": datetime.now().isoformat()
            })

            salvar_dados(dados)
            return u

    return {'erro': 'Usuário não encontrado'}

def sacar(id, valor):
    dados = carregar_dados()

    for u in dados['usuarios']:
        if u['id'] == id:
            if valor <= 0:
                return {'erro': 'Valor inválido'}
            
            if valor > u['saldo']:
                return {'erro': 'Saldo insuficiente'}

            u['saldo'] -= valor
            u['historico'].append({
                "tipo": "saque",
                "valor": valor,
                "data": datetime.now().isoformat()
            })

            salvar_dados(dados)
            return u

    return {'erro': 'Usuário não encontrado'}

def saldo(id):
    dados = carregar_dados()

    for u in dados['usuarios']:
        if u['id'] == id:
            return {
                'usuario': u['nome'],
                'saldo': u['saldo']
            }

    return {'erro': 'Usuário não encontrado'}


def extrato(id):
    dados = carregar_dados()

    for u in dados['usuarios']:
        if u['id'] == id:
            return {
                'usuario': u['nome'],
                'saldo': u['saldo'],
                'historico': u['historico']
            }

    return {'erro': 'Usuário não encontrado'}