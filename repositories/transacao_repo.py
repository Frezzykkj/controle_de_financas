from database.connection import get_connection

def adicionar_transacao_db(valor, tipo, categoria, comentario, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO transacoes (valor, tipo, categoria, comentario, data)
    VALUES (?, ?, ?, ?, ?)
    """, (valor, tipo, categoria, comentario, data))
    
    conn.commit()
    conn.close()

def listar_transacoes_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM transacoes")
    transacoes = cursor.fetchall()
    conn.close()
    return transacoes

def calcular_resumo_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'entrada'")
    saldo_entrada = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE tipo = 'saida'")
    saldo_saida = cursor.fetchone()[0] or 0
    
    saldo_total = saldo_entrada - saldo_saida
    
    conn.close()
    return saldo_entrada, saldo_saida, saldo_total

def calcular_por_categoria_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE categoria = 'alimentação' AND tipo = 'saida'")
    totais["alimentação"] = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(valor) FROM transacoes WHERE categoria = '' AND tipo = 'saida'")
    totais["alimentação"] = cursor.fetchone()[0] or 0
    totais = {}