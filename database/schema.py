from database.connection import get_connection

def criar_banco():
    conn = get_connection()
                 
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
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS transacoes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    valor REAL,
    tipo TEXT,
    categoria TEXT,
    comentario TEXT,
    data TEXT
    )
""")
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS categorias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    usuario_id INTEGER
    )
""")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS limites (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria_id INTEGER,
    valor REAL,
    mes TEXT, -- "2026-05"
    usuario_id INTEGER
    )
""")
    
    conn.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario text UNIQUE,
    email text UNIQUE,
    senha text
    )
""")
    
    conn.commit()
    conn.close()

