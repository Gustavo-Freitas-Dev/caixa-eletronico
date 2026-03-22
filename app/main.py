from fastapi import FastAPI
from services.user_service import criar_usuario, login_usuario
from services.bank_service import depositar, sacar, saldo, extrato
from database.usuario_model import Usuario
from database.login_model import Login

app = FastAPI()

@app.get('/')
def home():
    return {'message': 'API no ar'}

@app.post('/criar-usuario')
def criar(user: Usuario):
    return criar_usuario(user.dict())

@app.post('/login')
def login(user: Login):
    return login_usuario(user)

@app.post('/depositar')
def dep(id: int, valor: float):
    return depositar(id, valor)
