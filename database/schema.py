from database.connection import get_connection

def criar_banco():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario     TEXT    UNIQUE NOT NULL,
            email       TEXT    UNIQUE NOT NULL,
            senha       TEXT    NOT NULL,
            tipo_perfil TEXT    DEFAULT 'Apenas Financeiro'
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS categorias (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            nome       TEXT    NOT NULL,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS transacoes (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            valor        REAL    NOT NULL,
            tipo         TEXT    NOT NULL,
            categoria_id INTEGER,
            comentario   TEXT,
            data         TEXT    NOT NULL,
            usuario_id   INTEGER NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias (id),
            FOREIGN KEY (usuario_id)   REFERENCES usuarios   (id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente    TEXT    NOT NULL,
            tipo       TEXT    NOT NULL,
            valor_total REAL   NOT NULL,
            comentario TEXT,
            data       TEXT    NOT NULL,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS parcelas (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id   INTEGER NOT NULL,
            valor      REAL    NOT NULL,
            status     TEXT    NOT NULL DEFAULT 'pendente',
            data       TEXT    NOT NULL,
            usuario_id INTEGER NOT NULL,
            FOREIGN KEY (venda_id)   REFERENCES vendas   (id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS limites (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL,
            valor        REAL    NOT NULL,
            mes          TEXT    NOT NULL,
            usuario_id   INTEGER NOT NULL,
            UNIQUE (categoria_id, mes, usuario_id),
            FOREIGN KEY (categoria_id) REFERENCES categorias (id),
            FOREIGN KEY (usuario_id)   REFERENCES usuarios   (id)
        )
    """)

    conn.commit()
    conn.close()
