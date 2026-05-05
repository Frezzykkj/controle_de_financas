import bcrypt

def hash_senha(senha):
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

def verificar_senha(senha, hash):
    return bcrypt.checkpw(senha.encode("utf-8"), hash)