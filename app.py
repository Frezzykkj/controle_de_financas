import pandas as pd
import datetime
import streamlit as st
from database.schema import criar_banco
from services.auth_service import registrar, login
from repositories.transacao_repo import adicionar_transacao_db, listar_transacoes_db, calcular_resumo_db
from repositories.venda_repo import adicionar_venda_db, listar_vendas_db
from repositories.parcela_repo import adicionar_parcela_db, listar_parcelas_por_cliente_db, marcar_pago_db, calcular_total_pagos_db, buscar_valor_total_db

criar_banco()

# ───────────────────────────────────────────
# TELA DE LOGIN / CADASTRO
# ───────────────────────────────────────────
if "usuario_id" not in st.session_state:

    st.title("💸 Finance App")

    aba_login, aba_cadastro = st.tabs(["Entrar", "Criar conta"])

    with aba_login:
        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")

        if st.button("Entrar"):
            resultado = login(email, senha)
            if resultado:
                st.session_state["usuario_id"] = resultado[0]
                st.session_state["usuario_nome"] = resultado[1]
                st.rerun()
            else:
                st.error("Email ou senha incorretos.")

    with aba_cadastro:
        novo_usuario = st.text_input("Nome de usuário", key="cadastro_usuario")
        novo_email = st.text_input("Email", key="cadastro_email")
        nova_senha = st.text_input("Senha", type="password", key="cadastro_senha")

        if st.button("Criar conta"):
            try:
                registrar(novo_usuario, novo_email, nova_senha)
                st.success("Conta criada com sucesso! Faça login.")
            except Exception as e:
                st.error(f"Erro ao criar conta: {e}")

# ───────────────────────────────────────────
# APP PRINCIPAL (usuário logado)
# ───────────────────────────────────────────
else:
    usuario_id = st.session_state["usuario_id"]
    usuario_nome = st.session_state["usuario_nome"]

    st.sidebar.title(f"Olá, {usuario_nome}! 👋")
    if st.sidebar.button("Sair"):
        st.session_state.clear()
        st.rerun()

    aba1, aba2 = st.tabs(["💰 Financeiro", "🛠️ Serviços"])

    # ───────────────────────────────────────────
    # ABA FINANCEIRO
    # ───────────────────────────────────────────
    with aba1:
        st.title("Resumo Financeiro")

        saldo_entrada, saldo_saida, saldo_total = calcular_resumo_db()

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Saldo total", f"R$ {saldo_total:.2f}")
        with col2:
            st.metric("Total de entradas", f"R$ {saldo_entrada:.2f}")
        with col3:
            st.metric("Total de saídas", f"R$ {saldo_saida:.2f}")

        st.title("Adicionar transação")

        valor = st.number_input("Valor:", key="valor_transacao")
        tipo = st.selectbox("Tipo:", ["entrada", "saida"])
        categoria = None
        if tipo == "saida":
            categoria = st.text_input("Categoria:", key="categoria_transacao")
        comentario = st.text_input("Comentário (opcional):", key="comentario_transacao")
        data = st.date_input("Data:", value=datetime.date.today(), key="data_transacao")

        if st.button("Adicionar transação"):
            adicionar_transacao_db(valor, tipo, categoria, comentario, str(data))
            st.success("Transação adicionada com sucesso!")
            st.rerun()

        st.title("Transações registradas")
        transacoes = listar_transacoes_db()
        df = pd.DataFrame(transacoes, columns=["id", "valor", "tipo", "categoria", "comentario", "data", "id_usuario"])
        st.dataframe(df)

    # ───────────────────────────────────────────
    # ABA SERVIÇOS
    # ───────────────────────────────────────────
    with aba2:
        st.title("Adicionar venda")

        cliente = st.text_input("Nome do cliente:", key="cliente_servico")
        tipo_servico = st.selectbox("Tipo:", ["Manutenção", "Venda", "Empréstimo"], key="tipo_servico")
        valor_servico = st.number_input("Valor:", key="valor_servico")
        comentario_servico = st.text_input("Comentário (opcional):", key="comentario_servico")
        data_servico = st.date_input("Data:", value=datetime.date.today(), key="data_servico")

        if st.button("Adicionar venda"):
            adicionar_venda_db(cliente, tipo_servico, valor_servico, comentario_servico, str(data_servico))
            st.success("Venda adicionada com sucesso!")
            st.rerun()

        st.title("Vendas registradas")
        vendas = listar_vendas_db()
        df_vendas = pd.DataFrame(vendas, columns=["id", "cliente", "tipo", "valor_total", "comentario", "data", "id_usuario"])
        st.dataframe(df_vendas)

        st.title("Consultar parcelas")
        nCliente = st.text_input("Nome do cliente:", key="cliente_parcelas")

        if st.button("Listar parcelas"):
            ppc = listar_parcelas_por_cliente_db(nCliente)
            df_parcelas = pd.DataFrame(ppc, columns=["id", "venda_id", "valor", "status", "data"])
            st.dataframe(df_parcelas)

            total_pago = calcular_total_pagos_db(nCliente)
            valor_venda = buscar_valor_total_db(nCliente)
            valor_faltando = valor_venda - total_pago

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total pago", f"R$ {total_pago:.2f}")
            with col2:
                st.metric("Valor da venda", f"R$ {valor_venda:.2f}")
            with col3:
                st.metric("Ainda falta", f"R$ {valor_faltando:.2f}")

        st.title("Marcar parcela como paga")
        parcela_id = st.number_input("ID da parcela:", key="parcela_id_status")
        if st.button("Atualizar status"):
            marcar_pago_db(parcela_id)
            st.success("Status atualizado com sucesso!")
            st.rerun()

        st.title("Adicionar parcelas à venda")
        venda_id = st.number_input("ID da venda:", key="venda_id_parcelas")
        quantidade = st.selectbox("Quantidade de parcelas:", [1, 2, 3, 4, 5, 6])
        valor_parcela = st.number_input("Valor de cada parcela:", key="valor_parcela")
        status_parcela = st.selectbox("Status:", ["pendente", "pago"])
        data_parcela = st.date_input("Data:", value=datetime.date.today(), key="data_parcela")

        if st.button("Adicionar parcelas"):
            adicionar_parcela_db(venda_id, quantidade, valor_parcela, status_parcela, str(data_parcela))
            st.success("Parcelas adicionadas com sucesso!")
            st.rerun()