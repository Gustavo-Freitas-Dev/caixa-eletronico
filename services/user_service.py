from database.models import carregar_dados, salvar_dados
from utils.security import gerar_hash_senha, verificar_senha
from datetime import datetime

def criar_usuario(data: dict):
    dados = carregar_dados()

    # 🔍 Validação de campos obrigatórios
    campos_obrigatorios = ['nome', 'usuario', 'email', 'senha', 'cpf', 'telefone']
    
    for campo in campos_obrigatorios:
        if campo not in data:
            return {'erro': f'Campo obrigatório ausente: {campo}'}

    # 🔍 Validação de duplicidade
    for u in dados['usuarios']:
        if u['usuario'] == data['usuario']:
            return {'erro': 'Usuário já existe'}
        
        if u['email'] == data['email']:
            return {'erro': 'Email já cadastrado'}
        
        if u['cpf'] == data['cpf']:
            return {'erro': 'CPF já cadastrado'}

    # 🆕 Criar usuário
    novo_usuario = {
        'id': len(dados['usuarios']) + 1,
        'nome': data['nome'],
        'usuario': data['usuario'],
        'email': data['email'],
        'senha': gerar_hash_senha(data['senha']),
        'cpf': data['cpf'],
        'telefone': data['telefone'],
        'saldo': 0,
        'historico': [],
        'ativo': True,
        'data_criacao': datetime.now().isoformat(),
        'ultimo_login': None,
        'bloqueado': False
    }

    dados['usuarios'].append(novo_usuario)
    salvar_dados(dados)

    return novo_usuario


def login_usuario(data):
    dados = carregar_dados()

    for u in dados['usuarios']:
        if u['usuario'] == data.usuario:  # 👈 acessa direto

            if u.get('bloqueado'):
                return {'erro': 'Usuário bloqueado'}

            if verificar_senha(data.senha, u['senha']):
                u['ultimo_login'] = datetime.now().isoformat()
                salvar_dados(dados)

                return {
                    'message': 'Login realizado com sucesso',
                    'usuario': u['nome']
                }

            else:
                return {'erro': 'Senha incorreta'}

    return {'erro': 'Usuário não encontrado'}