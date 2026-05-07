from database.connection import get_connection

def adicionar_parcela_db(venda_id, quantidade, valor, status, data, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    for i in range(quantidade):
        cursor.execute("""
        INSERT INTO parcelas (venda_id, valor, status, data, usuario_id)
        VALUES (?, ?, ?, ?, ?)
        """, (venda_id, valor, status, data, usuario_id))
    conn.commit()
    conn.close()

def listar_parcelas_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parcelas")
    parcelas = cursor.fetchall()
    conn.close()
    return parcelas

def listar_parcelas_por_cliente_db(cliente, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT parcelas.* FROM parcelas
    JOIN vendas ON parcelas.venda_id = vendas.id
    WHERE vendas.cliente = ? AND vendas.usuario_id = ?
    """, (cliente, usuario_id))
    parcelas = cursor.fetchall()
    conn.close()
    return parcelas

def atualizar_parcela_db(parcela_id, valor, data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE parcelas
    SET valor = ?, data = ?
    WHERE id = ?
    """, (valor, data, parcela_id))
    conn.commit()
    conn.close()

def marcar_pago_db(parcela_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE parcelas
    SET status = 'pago'
    WHERE id = ?
    """, (parcela_id,))
    conn.commit()
    conn.close()

def calcular_total_pagos_db(cliente, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT sum(parcelas.valor) FROM parcelas
    JOIN vendas ON parcelas.venda_id = vendas.id
    WHERE vendas.cliente = ? AND parcelas.status = 'pago' AND vendas.usuario_id = ?
    """, (cliente, usuario_id))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] or 0

def buscar_valor_total_db(cliente, usuario_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT sum(valor_total) FROM vendas
    WHERE vendas.cliente = ? AND vendas.usuario_id = ?
    """, (cliente, usuario_id)) 
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] or 0