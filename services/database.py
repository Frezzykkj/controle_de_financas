import sqlite3

def criar_banco():
    conn = sqlite3.connect("storage/banco.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cliente TEXT,
        tipo TEXT,
        valor_total REAL,
        comentario TEXT,
        data TEXT
    )
                 
""")
    conn.execute("""
    CREATE TABLE IF NOT EXISTS parcelas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        venda_id INTEGER,
        valor REAL,
        status TEXT,
        data TEXT,
        FOREIGN KEY (venda_id) REFERENCES vendas (id)
    )
                 
""")
    
    conn.commit()
    conn.close()

def adicionar_venda(cliente, tipo, valor_total, comentario, data):
    conn = sqlite3.connect("storage/banco.db")
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO vendas (cliente, tipo, valor_total, comentario, data)
    VALUES (?, ?, ?, ?, ?)
    """, (cliente, tipo, valor_total, comentario, data))
    venda_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    return venda_id

def listar_vendas():
    conn = sqlite3.connect("storage/banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vendas")
    vendas = cursor.fetchall()
    conn.close()
    return vendas

def adicionar_parcela(venda_id, quantidade, valor, status, data):
    conn = sqlite3.connect("storage/banco.db")
    cursor = conn.cursor()
    for i in range(quantidade):
        cursor.execute("""
        INSERT INTO parcelas (venda_id, valor, status, data)
        VALUES (?, ?, ?, ?)
        """, (venda_id, valor, status, data))
    conn.commit()
    conn.close()

def listar_parcelas():
    conn = sqlite3.connect("storage/banco.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM parcelas")
    parcelas = cursor.fetchall()
    conn.close()
    return parcelas

def listar_parcelas_por_cliente(cliente):
    conn = sqlite3.connect("storage/banco.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT parcelas.* FROM parcelas
    JOIN vendas ON parcelas.venda_id = vendas.id
    WHERE vendas.cliente = ?
    """, (cliente,))
    parcelas = cursor.fetchall()
    conn.close()
    return parcelas

def atualizar_parcela(parcela_id, valor, data):
    conn = sqlite3.connect("storage/banco.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE parcelas
    SET valor = ?, data = ?
    WHERE id = ?
    """, (valor, data, parcela_id))
    conn.commit()
    conn.close()

def marcar_pago(parcela_id):
    conn = sqlite3.connect("storage/banco.db")
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE parcelas
    SET status = 'pago'
    WHERE id = ?
    """, (parcela_id,))
    conn.commit()
    conn.close()

def calcular_total_pagos(cliente):
    conn = sqlite3.connect("storage/banco.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT sum(parcelas.valor) FROM parcelas
    JOIN vendas ON parcelas.venda_id = vendas.id
    WHERE vendas.cliente = ? AND parcelas.status = 'pago'
    """, (cliente,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] or 0

def buscar_valor_total(cliente):
    conn = sqlite3.connect("storage/banco.db")
    cursor = conn.cursor()
    cursor.execute("""
    SELECT valor_total FROM vendas
    WHERE vendas.cliente = ?
    """, (cliente,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] or 0