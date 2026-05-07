from repositories.usuario_repo import cadastro_usuario, buscar_usuario
from utils.security import verificar_senha
import re

def validar_email(email):
    padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    # re.match verifica se o e-mail segue o padrão
    if re.match(padrao, email):
        return True
    return False

def registrar(usuario, email, senha):
    if not validar_email(email):
        raise Exception("O formato do e-mail não é válido. Use algo como nome@exemplo.com")
    
    cadastro_usuario(usuario, email, senha)

def login(email, senha):
    usuario = buscar_usuario(email)
    if usuario is None:
        return None
    senha_hash = usuario[3]
    if verificar_senha(senha, senha_hash):
        return usuario
    return None