from fastapi import FastAPI

app = FastAPI()

saldo = 0
historico = []

@app.get('/')
def home():
    return{'message': 'A API está no ar!'}

@app.get('/saldo')
def ver_saldo():
    return{'saldo': saldo}

@app.post('/depositar')
def depositar(valor:float):
    global saldo

    saldo += valor
    historico.append(f'-{valor}')


    return {
        'mensagem': 'Depósito realizado',
        'Valor depósitado': valor
        }   

@app.post('/sacar')
def sacar(valor:float):
    global saldo, historico

    if saldo <= 0:
        return {'ERROR': 'Saldo inexistente.'}
    elif valor > saldo:
        return {'ERROR': 'Saldo insuficiente.'}
    else:
        saldo -= valor
        historico.append(f'-{valor}')

        return {
            'message': 'Saque realizado com sucesso!',
            'valor sacado': valor
        }

@app.get('/extrato')
def ver_historico():
    return {
        'saldo': saldo,
        'historico': historico
    }