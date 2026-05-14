from database.connection import get_connection

def definir_limite(categoria_id: int, valor: float, mes: str, usuario_id: int):
    """Cria ou atualiza o limite de uma categoria para um mês. Ex: mes = '2026-05'"""
    conn = get_connection()
    conn.execute("""
        INSERT INTO limites (categoria_id, valor, mes, usuario_id)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(categoria_id, mes, usuario_id) DO UPDATE SET valor = excluded.valor
    """, (categoria_id, valor, mes, usuario_id))
    conn.commit()
    conn.close()

def listar_limites_do_mes(mes: str, usuario_id: int) -> list[tuple]:
    """Retorna lista de (categoria_nome, valor_limite, gasto_atual)."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.nome,
               l.valor AS limite,
               COALESCE(SUM(t.valor), 0) AS gasto
        FROM limites l
        JOIN categorias c ON c.id = l.categoria_id
        LEFT JOIN transacoes t
            ON t.categoria_id = l.categoria_id
            AND t.usuario_id  = l.usuario_id
            AND strftime('%Y-%m', t.data) = l.mes
            AND t.tipo = 'saida'
        WHERE l.mes = ? AND l.usuario_id = ?
        GROUP BY l.categoria_id
        ORDER BY c.nome
    """, (mes, usuario_id))
    resultado = cursor.fetchall()
    conn.close()
    return resultado
