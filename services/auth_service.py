from repositories.usuario_repo import cadastro_usuario, buscar_usuario
from utils.security import verificar_senha

def registrar(usuario, email, senha):
    cadastro_usuario(usuario, email, senha)

def login(email, senha):
    usuario = buscar_usuario(email)
    if usuario is None:
        return None
    senha_hash = usuario[3]
    if verificar_senha(senha, senha_hash):
        return usuario
    return None