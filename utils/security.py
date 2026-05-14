import bcrypt

def hash_senha(senha: str) -> bytes:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

def verificar_senha(senha: str, hash_salvo: bytes) -> bool:
    return bcrypt.checkpw(senha.encode("utf-8"), hash_salvo)
