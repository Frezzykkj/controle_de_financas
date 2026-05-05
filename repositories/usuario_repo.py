from database.connection import get_connection
from utils.security import verificar_senha, hash_senha

def cadastro_usuario(usuario, email, senha):
    conn = get_connection()
    cursor = conn.cursor()
    senha = hash_senha(senha)
    cursor.execute("""
    INSERT INTO usuarios (usuario, email, senha)
    VALUES (?, ?, ?)
    """, (usuario, email, senha))
    
    conn.commit()
    conn.close()

def buscar_usuario(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM usuarios WHERE email = ?
    """, (email,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado
    