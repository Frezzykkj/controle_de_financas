from database.connection import get_connection

def mudar_limite_db(categoria, valor_limite):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO limites (categoria, valor_limite)
    VALUES (?, ?)
    """, (categoria, valor_limite))
    conn.commit()
    conn.close()

def carregar_limites_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT categoria, valor_limite FROM limites")
    resultado = cursor.fetchall()
    conn.close()
    return {categoria: valor for categoria, valor in resultado}