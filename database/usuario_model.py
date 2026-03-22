from pydantic import BaseModel, EmailStr

class Usuario(BaseModel):
    nome: str
    usuario: str
    email: EmailStr
    senha: str
    cpf: str
    telefone: str