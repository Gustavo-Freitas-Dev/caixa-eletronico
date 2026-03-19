from fastapi import FastAPI

app = FastAPI()

contador_id = 1
usuarios = []

@app.get('/')
def home():
    return{'message': 'A API está no ar!'}

@app.post('/criar-usuario')
def criar_usuario(usuario:str):
    global contador_id

    usuario = {
        'id': contador_id,
        'usuario': usuario,
        'saldo': 0,
        'historico': [],
        'ativo': True
    }

    usuarios.append(usuario)
    contador_id += 1

@app.get('/vizualizar_usuarios')
def visualizar_usuarios():
    return usuarios

@app.get('/saldo')
def ver_saldo(id:int):
    global usuarios

    for usuario in usuarios:
        if usuario['id'] == id:  
            return usuario
        
    return {"erro": "Usuário não encontrado"}


@app.post('/depositar')
def depositar(id:int, valor:float):
    global usuarios

    for usuario in usuarios:
        if usuario['id'] == id:
            usuario['saldo'] += valor
            usuario['historico'].append(f'DEPÓSITO +{valor}')

    return {
        'mensagem': 'Depósito realizado',
        'Valor depósitado': valor
        }   

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