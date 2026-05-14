"""
Execute este script UMA VEZ para migrar o banco existente.
Como rodar:  python migrar_banco.py
"""
import sqlite3
import os

DB_PATH = os.path.join("storage", "banco.db")
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ── transacoes ──────────────────────────────────────────────
cursor.execute("PRAGMA table_info(transacoes)")
colunas = [row[1] for row in cursor.fetchall()]
if "categoria_id" not in colunas:
    conn.execute("ALTER TABLE transacoes ADD COLUMN categoria_id INTEGER")
    print("✅ categoria_id adicionada em 'transacoes'.")

# ── parcelas ─────────────────────────────────────────────────
cursor.execute("PRAGMA table_info(parcelas)")
if "usuario_id" not in [row[1] for row in cursor.fetchall()]:
    conn.execute("ALTER TABLE parcelas ADD COLUMN usuario_id INTEGER")
    print("✅ usuario_id adicionada em 'parcelas'.")

# ── vendas ───────────────────────────────────────────────────
cursor.execute("PRAGMA table_info(vendas)")
if "usuario_id" not in [row[1] for row in cursor.fetchall()]:
    conn.execute("ALTER TABLE vendas ADD COLUMN usuario_id INTEGER")
    print("✅ usuario_id adicionada em 'vendas'.")

# ── usuarios ─────────────────────────────────────────────────
cursor.execute("PRAGMA table_info(usuarios)")
if "tipo_perfil" not in [row[1] for row in cursor.fetchall()]:
    conn.execute("ALTER TABLE usuarios ADD COLUMN tipo_perfil TEXT DEFAULT 'Apenas Financeiro'")
    print("✅ tipo_perfil adicionada em 'usuarios'.")

# ── limites: recriar com UNIQUE ───────────────────────────────
# SQLite não permite ALTER TABLE para adicionar constraints.
# Solução padrão: renomear antiga → criar nova correta → copiar dados → apagar antiga.
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='limites'")
if cursor.fetchone():
    conn.executescript("""
        ALTER TABLE limites RENAME TO limites_old;

        CREATE TABLE limites (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria_id INTEGER NOT NULL,
            valor        REAL    NOT NULL,
            mes          TEXT    NOT NULL,
            usuario_id   INTEGER NOT NULL,
            UNIQUE (categoria_id, mes, usuario_id)
        );

        INSERT INTO limites (id, categoria_id, valor, mes, usuario_id)
        SELECT id, categoria_id, valor, mes, usuario_id FROM limites_old;

        DROP TABLE limites_old;
    """)
    print("✅ Tabela 'limites' recriada com UNIQUE constraint.")

conn.commit()
conn.close()
print("\n✅ Migração concluída. Pode rodar o app normalmente.")