from datetime import date
from repositories.parcela_repo import marcar_parcela_paga, buscar_valor_parcela
from repositories.transacao_repo import adicionar_transacao

# categoria_id = None significa "sem categoria" — aceitável para entradas automáticas
# Em breve podemos criar uma categoria padrão "Recebimentos" e usar o ID dela aqui.

def registrar_pagamento_parcela(parcela_id: int, usuario_id: int) -> bool:
    sucesso = marcar_parcela_paga(parcela_id, usuario_id)
    if sucesso:
        valor = buscar_valor_parcela(parcela_id, usuario_id)
        adicionar_transacao(
            valor=valor,
            tipo='entrada',
            categoria_id=None,
            comentario=f'Parcela #{parcela_id} recebida',
            data=str(date.today()),
            usuario_id=usuario_id,
        )
    return sucesso
