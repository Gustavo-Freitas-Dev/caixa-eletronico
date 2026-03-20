from fastapi import FastAPI
from database.models import carregar_dados, salvar_dados

app = FastAPI()

contador_id = 1
usuarios = []

@app.get('/')
def home():
    return{'message': 'A API está no ar!'}

@app.get("/usuarios")
def listar():
    dados = carregar_dados()
    return dados

@app.post('/criar-usuario')
def criar_usuario(usuario:str):
    global contador_id
    dados = carregar_dados()

    novo_usuario = {
        'id': len(dados['usuarios']) + 1,
        'usuario': usuario,
        'saldo': 0,
        'historico': [],
        'ativo': True
    }

    dados['usuarios'].append(novo_usuario)
    salvar_dados(dados)
    return novo_usuario

@app.get('/vizualizar_usuarios')
def visualizar_usuarios():
    dados = carregar_dados()

    return dados

@app.get('/saldo')
def ver_saldo(id:int):
    dados = carregar_dados()

    for usuario in dados['usuarios']:
        if usuario['id'] == id:  
            return {
                'usuario': usuario['usuario'],
                'saldo': usuario['saldo']
            }
        
    return {"erro": "Usuário não encontrado"}


@app.post('/depositar')
def depositar(id:int, valor:float):
    if valor <=0:
        return {
            'erro': 'VALOR_INVALIDO',
            'mensagem': 'O valor do depósito deve ser maior que zero.'
        }, 400

    dados = carregar_dados()

    for usuario in dados['usuarios']:
        if usuario['id'] == id:
            usuario['saldo'] += valor
            usuario['historico'].append(f'DEPÓSITO +{valor}')

            salvar_dados(dados)
            return {
                'mensagem': 'Depósito realizado',
                'Valor depósitado': valor
                }
        
    return {
    'erro': 'ID_INEXISTENTE',
    'mensagem': f'Não foi encontrada nenhuma conta com o ID {id}.'
    }, 404

@app.post('/sacar')
def sacar(id:int, valor:float):
    global usuarios

    for usuario in usuarios:
        if usuario['id'] == id:
            if valor <= 0:
                return{'Erro': 'O valor de saque deve ser maior que zero.'}
            elif valor > usuario['saldo']:
                return {'Erro': 'Saldo insuficiente.'}
            else:
                usuario['saldo'] -= valor
                usuario['historico'].append(f'SAQUE: -{valor}')
                return {
                    'message': 'Saque realizado com sucesso!',
                    'valor sacado': valor
                }

@app.get('/extrato')
def ver_historico(id:int):
    global usuarios

    for usuario in usuarios:
        if usuario['id'] == id:
            return {
                'usuario': usuario['usuario'],
                'saldo': usuario['saldo'],
                'historico': usuario['historico']
            }