from database.connection import get_connection

def adicionar_venda_db(cliente, tipo, valor_total, comentario, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO vendas (cliente, tipo, valor_total, comentario, data)
    VALUES (?, ?, ?, ?, ?)
    """, (cliente, tipo, valor_total, comentario, data))
    venda_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return venda_id

def listar_vendas_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendas")
    vendas = cursor.fetchall()
    conn.close()
    return vendas

