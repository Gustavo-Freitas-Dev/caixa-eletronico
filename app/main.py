from fastapi import FastAPI
from database.models import carregar_dados, salvar_dados
from datetime import datetime
from utils.services import gerar_hash_senha, verificar_senha

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

from datetime import datetime

from datetime import datetime

@app.post('/criar-usuario')
def criar_usuario(
    nome: str,
    usuario: str,
    email: str,
    senha: str,
    cpf: str,
    telefone: str
):
    dados = carregar_dados()

    # 🔍 Validação
    for u in dados['usuarios']:
        if u['usuario'] == usuario:
            return {'ERRO': 'Usuário já existe'}
        
        if u['email'] == email:
            return {'ERRO': 'Email já cadastrado'}
        
        if u['cpf'] == cpf:
            return {'ERRO': 'CPF já cadastrado'}

    novo_usuario = {
        'id': len(dados['usuarios']) + 1,
        'nome': nome,
        'usuario': usuario,
        'email': email,
        'senha': gerar_hash_senha(senha),
        'cpf': cpf,
        'telefone': telefone,
        'saldo': 0,
        'historico': [],
        'ativo': True,
        'data_criacao': datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        'ultimo_login': None,
        'bloqueado': False
    }

    dados['usuarios'].append(novo_usuario)
    salvar_dados(dados)

    return novo_usuario

@app.post('/login')
def login(usuario:str, senha:str):
    dados = carregar_dados()

    for user in dados['usuarios']:
        if user['usuario'] == usuario:
            if verificar_senha(senha, user['senha']):
                return {'message': 'Login realizado com sucesso!'}
    
    return {'ERRO': 'Login incorreto.'}

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
                'usuario': usuario['nome'],
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
            usuario['historico'].append(f'DEPÓSITO | R$ {valor:.2f} | {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

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
    dados = carregar_dados()

    for usuario in dados['usuarios']:
        if usuario['id'] == id:
            if valor <= 0:
                return{'Erro': 'O valor de saque deve ser maior que zero.'}
            elif valor > usuario['saldo']:
                return {'Erro': 'Saldo insuficiente.'}
            else:
                usuario['saldo'] -= valor
                usuario['historico'].append(f'  SAQUE  | R$ {valor:.2f} | {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')

                salvar_dados(dados)
                return {
                    'message': 'Saque realizado com sucesso!',
                    'valor sacado': valor
                }
            
    return {
    'erro': 'ID_INEXISTENTE',
    'mensagem': f'Não foi encontrada nenhuma conta com o ID {id}.'
    }, 404


@app.get('/extrato')
def ver_historico(id:int):
    dados = carregar_dados()

    for usuario in dados['usuarios']:
        if usuario['id'] == id:
            return {
                'usuario': usuario['nome'],
                'saldo': usuario['saldo'],
                'historico': usuario['historico']
            }    