import bcrypt

def gerar_hash_senha(senha: str) -> str:
    senha_bytes = senha.encode('utf-8')
    hash_senha = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
    return hash_senha.decode('utf-8')

def verificar_senha(senha_digitada: str, senha_hash: str) -> bool:
    return bcrypt.checkpw(
        senha_digitada.encode('utf-8'),
        senha_hash.encode('utf-8')
    )

def validar_cpf(cpf: str) -> bool:
    # Remove tudo que não for número
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica tamanho
    if len(cpf) != 11:
        return False

    # Verifica se todos os números são iguais
    if cpf == cpf[0] * 11:
        return False

    # ======================
    # 1º dígito verificador
    # ======================
    soma = 0
    peso = 10

    for num in cpf[:9]:
        soma += int(num) * peso
        peso -= 1

    resto = soma % 11

    if resto < 2:
        digito1 = 0
    else:
        digito1 = 11 - resto

    # ======================
    # 2º dígito verificador
    # ======================
    soma = 0
    peso = 11

    for num in cpf[:10]:
        soma += int(num) * peso
        peso -= 1

    resto = soma % 11

    if resto < 2:
        digito2 = 0
    else:
        digito2 = 11 - resto

    # ======================
    # Comparação final
    # ======================
    return cpf[-2:] == f"{digito1}{digito2}"