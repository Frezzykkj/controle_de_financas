from database.connection import get_connection

def adicionar_transacao_db(valor, tipo, categoria, comentario, data, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO transacoes (valor, tipo, categoria, comentario, data, usuario_id)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (valor, tipo, categoria, comentario, data, usuario_id))
    
    conn.commit()
    conn.close()

def listar_transacoes_db(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, valor, tipo, categoria, comentario, data
    FROM transacoes
    WHERE usuario_id = ?
    """, (usuario_id,))
    dados = cursor.fetchall()
    conn.close()
    return dados

def calcular_resumo_db(usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'entrada' AND usuario_id = ?", (usuario_id,))
    saldo_entrada = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'saida' AND usuario_id = ?", (usuario_id,))
    saldo_saida = cursor.fetchone()[0] or 0
    
    saldo_total = saldo_entrada - saldo_saida
    conn.close()
    return saldo_entrada, saldo_saida, saldo_total