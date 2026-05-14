import datetime
import pandas as pd
import streamlit as st

from database.schema import criar_banco
from services.auth_service import registrar, login
from services.financeiro_service import registrar_pagamento_parcela
from repositories.transacao_repo import adicionar_transacao, listar_transacoes, calcular_resumo
from repositories.venda_repo import adicionar_venda, listar_vendas, listar_clientes
from repositories.parcela_repo import (
    adicionar_parcelas,
    listar_parcelas_por_cliente,
    calcular_total_pago,
    buscar_valor_total_vendas,
)
from repositories.categoria_repo import (
    criar_categoria, listar_categorias,
    deletar_categoria, renomear_categoria,
)
from repositories.limite_repo import definir_limite, listar_limites_do_mes
from repositories.dashboard_repo import (
    lucro_por_periodo,
    total_a_receber,
    a_receber_por_cliente,
)

criar_banco()

# ─────────────────────────────────────────────────────────────
# TELA DE LOGIN / CADASTRO
# ─────────────────────────────────────────────────────────────
if "usuario_id" not in st.session_state:
    st.title("💸 Finance App")

    aba_login, aba_cadastro = st.tabs(["Entrar", "Criar conta"])

    with aba_login:
        email = st.text_input("Email", key="login_email")
        senha = st.text_input("Senha", type="password", key="login_senha")
        if st.button("Entrar"):
            resultado = login(email, senha)
            if resultado:
                st.session_state["usuario_id"]   = resultado[0]
                st.session_state["usuario_nome"] = resultado[1]
                st.session_state["tipo_perfil"]  = resultado[4]
                st.rerun()
            else:
                st.error("Email ou senha incorretos.")

    with aba_cadastro:
        novo_usuario = st.text_input("Nome de usuário", key="cadastro_usuario")
        novo_email   = st.text_input("Email",           key="cadastro_email")
        nova_senha   = st.text_input("Senha", type="password", key="cadastro_senha")
        tipo_perfil  = st.selectbox(
            "Como você vai usar o app?",
            ["Apenas Financeiro", "Autônomo (Serviços)", "Motorista / Entregador"],
            key="cadastro_perfil",
        )
        if st.button("Criar conta"):
            try:
                registrar(novo_usuario, novo_email, nova_senha, tipo_perfil)
                st.success("Conta criada! Faça login.")
            except ValueError as e:
                st.error(str(e))
            except Exception as e:
                st.error(f"Erro: {e}")

# ─────────────────────────────────────────────────────────────
# APP PRINCIPAL
# ─────────────────────────────────────────────────────────────
else:
    usuario_id   = st.session_state["usuario_id"]
    usuario_nome = st.session_state["usuario_nome"]
    tipo_perfil  = st.session_state.get("tipo_perfil", "Apenas Financeiro")

    st.sidebar.title(f"Olá, {usuario_nome}! 👋")
    st.sidebar.caption(f"Perfil: {tipo_perfil}")
    if st.sidebar.button("Sair"):
        st.session_state.clear()
        st.rerun()

    tem_servicos = tipo_perfil in ("Autônomo (Serviços)", "Motorista / Entregador")
    nomes_abas = ["📊 Dashboard", "💰 Financeiro", "🏷️ Categorias"]
    if tem_servicos:
        nomes_abas.append("🛠️ Serviços")

    abas = st.tabs(nomes_abas)
    aba_dashboard   = abas[0]
    aba_financeiro  = abas[1]
    aba_categorias  = abas[2]
    aba_servicos    = abas[3] if tem_servicos else None

    # ──────────────────────────────────────────
    # ABA DASHBOARD
    # ──────────────────────────────────────────
    with aba_dashboard:
        st.header("Dashboard")

        st.subheader("Lucro por período")

        col_ini, col_fim = st.columns(2)
        with col_ini:
            data_inicio = st.date_input(
                "De:", value=datetime.date.today().replace(day=1), key="dash_inicio"
            )
        with col_fim:
            data_fim = st.date_input(
                "Até:", value=datetime.date.today(), key="dash_fim"
            )

        resumo = lucro_por_periodo(str(data_inicio), str(data_fim), usuario_id)

        col1, col2, col3 = st.columns(3)
        col1.metric("Entradas", f"R$ {resumo['entrada']:.2f}")
        col2.metric("Saídas",   f"R$ {resumo['saida']:.2f}")
        col3.metric("Lucro",    f"R$ {resumo['lucro']:.2f}")

        st.divider()

        st.subheader("A receber de clientes")

        total = total_a_receber(usuario_id)
        st.metric("Total de parcelas pendentes", f"R$ {total:.2f}")

        clientes_pendentes = a_receber_por_cliente(usuario_id)
        if clientes_pendentes:
            import pandas as pd
            df_pend = pd.DataFrame(clientes_pendentes, columns=["Cliente", "A receber (R$)"])
            st.dataframe(df_pend, use_container_width=True)
        else:
            st.info("Nenhuma parcela pendente no momento.")


    # ──────────────────────────────────────────
    # ABA FINANCEIRO
    # ──────────────────────────────────────────
    with aba_financeiro:
        st.header("Resumo Financeiro")
        entradas, saidas, saldo = calcular_resumo(usuario_id)

        col1, col2, col3 = st.columns(3)
        col1.metric("Saldo total",       f"R$ {saldo:.2f}")
        col2.metric("Total de entradas", f"R$ {entradas:.2f}")
        col3.metric("Total de saídas",   f"R$ {saidas:.2f}")

        st.divider()
        st.subheader("Adicionar transação")

        categorias = listar_categorias(usuario_id)
        # Mapa nome → id para o selectbox
        mapa_cats  = {nome: cid for cid, nome in categorias}

        valor      = st.number_input("Valor (R$):", min_value=0.01, format="%.2f", key="tr_valor")
        tipo       = st.selectbox("Tipo:", ["entrada", "saida"], key="tr_tipo")

        categoria_id = None
        if tipo == "saida":
            if mapa_cats:
                nome_cat     = st.selectbox("Categoria:", list(mapa_cats.keys()), key="tr_cat")
                categoria_id = mapa_cats[nome_cat]
            else:
                st.info("Nenhuma categoria criada. Crie uma na aba 🏷️ Categorias.")

        comentario = st.text_input("Comentário (opcional):", key="tr_comentario")
        data       = st.date_input("Data:", value=datetime.date.today(), key="tr_data")

        if st.button("➕ Adicionar transação"):
            adicionar_transacao(valor, tipo, categoria_id, comentario, str(data), usuario_id)
            st.success("Transação adicionada!")
            st.rerun()

        st.divider()
        st.subheader("Histórico de transações")
        transacoes = listar_transacoes(usuario_id)
        if transacoes:
            df = pd.DataFrame(transacoes, columns=["ID", "Valor", "Tipo", "Categoria", "Comentário", "Data"])
            st.dataframe(df.drop(columns=["ID"]), use_container_width=True)
        else:
            st.info("Nenhuma transação registrada ainda.")

    # ──────────────────────────────────────────
    # ABA CATEGORIAS
    # ──────────────────────────────────────────
    with aba_categorias:
        st.header("Gerenciar Categorias")

        # ── Criar nova categoria ──
        st.subheader("Nova categoria")
        nova_cat = st.text_input("Nome:", key="cat_nova")
        if st.button("➕ Criar categoria"):
            if nova_cat.strip():
                criar_categoria(nova_cat, usuario_id)
                st.success(f"Categoria '{nova_cat}' criada!")
                st.rerun()
            else:
                st.warning("Digite um nome para a categoria.")

        st.divider()

        # ── Lista + ações ──
        categorias = listar_categorias(usuario_id)
        if categorias:
            st.subheader("Suas categorias")
            for cid, nome in categorias:
                col_nome, col_rename, col_del = st.columns([3, 2, 1])
                col_nome.write(f"🏷️ {nome}")

                novo_nome = col_rename.text_input("", key=f"rename_{cid}", placeholder="Renomear")
                if col_rename.button("✏️", key=f"btn_rename_{cid}"):
                    if novo_nome.strip():
                        renomear_categoria(cid, novo_nome, usuario_id)
                        st.rerun()

                if col_del.button("🗑️", key=f"btn_del_{cid}"):
                    deletar_categoria(cid, usuario_id)
                    st.rerun()

            st.divider()

            # ── Limites mensais ──
            st.subheader("Limites mensais por categoria")
            st.caption("Defina quanto pode gastar em cada categoria por mês.")

            mes_sel = st.date_input(
                "Mês de referência:", value=datetime.date.today(),
                key="limite_mes"
            )
            mes_str = mes_sel.strftime("%Y-%m")

            mapa_cats = {nome: cid for cid, nome in categorias}
            cat_limite = st.selectbox("Categoria:", list(mapa_cats.keys()), key="limite_cat")
            valor_lim  = st.number_input("Limite (R$):", min_value=0.01, format="%.2f", key="limite_valor")

            if st.button("💾 Salvar limite"):
                definir_limite(mapa_cats[cat_limite], valor_lim, mes_str, usuario_id)
                st.success(f"Limite de R$ {valor_lim:.2f} salvo para '{cat_limite}' em {mes_str}.")
                st.rerun()

            st.divider()

            # ── Painel de limites do mês ──
            st.subheader(f"Situação dos limites — {mes_str}")
            limites = listar_limites_do_mes(mes_str, usuario_id)
            if limites:
                for nome, limite, gasto in limites:
                    percentual = gasto / limite if limite > 0 else 0
                    if percentual >= 1.0:
                        icone, cor = "🔴", "red"
                    elif percentual >= 0.8:
                        icone, cor = "🟡", "orange"
                    else:
                        icone, cor = "🟢", "green"

                    st.write(f"{icone} **{nome}** — R$ {gasto:.2f} / R$ {limite:.2f}")
                    st.progress(min(percentual, 1.0))
            else:
                st.info("Nenhum limite definido para este mês ainda.")
        else:
            st.info("Crie sua primeira categoria acima para começar.")

    # ──────────────────────────────────────────
    # ABA SERVIÇOS
    # ──────────────────────────────────────────
    if aba_servicos:
        with aba_servicos:
            st.subheader("Adicionar venda / serviço")

            cliente       = st.text_input("Nome do cliente:", key="sv_cliente")
            tipo_servico  = st.selectbox("Tipo:", ["Manutenção", "Venda", "Empréstimo"], key="sv_tipo")
            valor_sv      = st.number_input("Valor (R$):", min_value=0.01, format="%.2f", key="sv_valor")
            comentario_sv = st.text_input("Comentário (opcional):", key="sv_comentario")
            data_sv       = st.date_input("Data:", value=datetime.date.today(), key="sv_data")

            if st.button("➕ Adicionar venda"):
                adicionar_venda(cliente, tipo_servico, valor_sv, comentario_sv, str(data_sv), usuario_id)
                st.success("Venda adicionada!")
                st.rerun()

            st.divider()
            st.subheader("Vendas registradas")
            vendas = listar_vendas(usuario_id)
            if vendas:
                df_v = pd.DataFrame(vendas, columns=["ID", "Cliente", "Tipo", "Valor", "Comentário", "Data"])
                st.dataframe(df_v, use_container_width=True)
            else:
                st.info("Nenhuma venda registrada ainda.")

            st.divider()
            st.subheader("Consultar parcelas por cliente")
            clientes_lista = listar_clientes(usuario_id)
            if clientes_lista:
                cliente_sel = st.selectbox("Selecione o cliente:", clientes_lista, key="pc_cliente")
                if st.button("🔍 Listar parcelas"):
                    parcelas = listar_parcelas_por_cliente(cliente_sel, usuario_id)
                    if parcelas:
                        df_p = pd.DataFrame(parcelas, columns=["ID", "ID Venda", "Valor", "Status", "Data"])
                        st.dataframe(df_p, use_container_width=True)
                        total_pago  = calcular_total_pago(cliente_sel, usuario_id)
                        valor_total = buscar_valor_total_vendas(cliente_sel, usuario_id)
                        c1, c2, c3  = st.columns(3)
                        c1.metric("Total pago",     f"R$ {total_pago:.2f}")
                        c2.metric("Valor da venda", f"R$ {valor_total:.2f}")
                        c3.metric("Ainda falta",    f"R$ {(valor_total - total_pago):.2f}")
                    else:
                        st.info("Nenhuma parcela encontrada.")
            else:
                st.info("Nenhum cliente cadastrado ainda.")

            st.divider()
            st.subheader("Registrar pagamento de parcela")
            st.caption("O valor é lançado automaticamente no financeiro.")
            parcela_id = st.number_input("ID da parcela:", min_value=1, step=1, key="pg_id")
            if st.button("✅ Marcar como paga"):
                sucesso = registrar_pagamento_parcela(int(parcela_id), usuario_id)
                if sucesso:
                    st.success("Pago e lançado no financeiro!")
                else:
                    st.warning("Parcela não encontrada ou já paga.")
                st.rerun()

            st.divider()
            st.subheader("Adicionar parcelas a uma venda")
            if vendas:
                opcoes  = {f"#{v[0]} — {v[1]} (R$ {v[3]:.2f})": v[0] for v in vendas}
                sel     = st.selectbox("Venda:", list(opcoes.keys()), key="pa_venda")
                qtd     = st.selectbox("Qtd de parcelas:", [1, 2, 3, 4, 5, 6, 12], key="pa_qtd")
                v_parc  = st.number_input("Valor cada (R$):", min_value=0.01, format="%.2f", key="pa_valor")
                st_parc = st.selectbox("Status inicial:", ["pendente", "pago"], key="pa_status")
                d_parc  = st.date_input("Data:", value=datetime.date.today(), key="pa_data")
                if st.button("➕ Adicionar parcelas"):
                    adicionar_parcelas(opcoes[sel], qtd, v_parc, st_parc, str(d_parc), usuario_id)
                    st.success(f"{qtd} parcela(s) adicionada(s)!")
                    st.rerun()
            else:
                st.info("Cadastre uma venda primeiro.")
