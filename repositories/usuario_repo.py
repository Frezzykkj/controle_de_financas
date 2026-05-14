from database.connection import get_connection
from utils.security import hash_senha

def cadastrar_usuario(usuario: str, email: str, senha: str, tipo_perfil: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO usuarios (usuario, email, senha, tipo_perfil)
        VALUES (?, ?, ?, ?)
    """, (usuario, email, hash_senha(senha), tipo_perfil))
    conn.commit()
    conn.close()

def buscar_usuario_por_email(email: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado

def buscar_perfil(usuario_id: int) -> str | None:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT tipo_perfil FROM usuarios WHERE id = ?", (usuario_id,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None
