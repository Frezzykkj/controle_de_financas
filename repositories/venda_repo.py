from database.connection import get_connection

def adicionar_venda_db(cliente, tipo, valor_total, comentario, data, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO vendas (cliente, tipo, valor_total, comentario, data, usuario_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (cliente, tipo, valor_total, comentario, data, usuario_id))
    venda_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return venda_id

def listar_vendas_db(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    # Filtramos para que o Usuário A não veja as vendas do Usuário B
    cursor.execute("SELECT id, cliente, tipo, valor_total, comentario, data FROM vendas WHERE usuario_id = ?", (usuario_id,))
    vendas = cursor.fetchall()
    conn.close()
    return vendas

