from services.database import adicionar_parcela, adicionar_venda, criar_banco, listar_parcelas, listar_parcelas_por_cliente, listar_vendas, marcar_pago

criar_banco()

import pandas as pd
import datetime
import streamlit as st
from services.logic import salvar_dados, transacoes, calcular_por_categoria, calcular_resumo, limites, salvar_limites, filtrar_por_periodo

aba1, aba2 = st.tabs(["💰 Financeiro", "🛠️ Serviços"])

with aba1:
    #resumo financeiro
    st.title("Resumo Financeiro")

    saldo_entrada, saldo_saida, saldo_total = calcular_resumo()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Saldo total", f"R$ {saldo_total:.2f}")

    with col2:
        st.metric("Valor total de entradas", f"R$ {saldo_entrada:.2f}")

    with col3:
        st.metric("Valor total de saídas", f"R$ {saldo_saida:.2f}")

    #resumo financeiro

    #adicionar transação
    st.title("Adicionar transação")

    valor = st.number_input("digite o valor:", key="valor_transacao")
    tipo = st.selectbox("qual o tipo da transação?", ["entrada", "saida"])
    if tipo == "entrada":
        categoria = None
    elif tipo == "saida":
        categoria = st.selectbox("qual a categoria da transação?", ["alimentação", "transporte", "lazer", "outros"])
    comentario = st.text_input("comentário (opcional)", key="comentario_transacao")
    data = st.date_input("data", value=datetime.date.today(), key="data_transacao")



    if st.button("adicionar"):
        transacoes.append({"valor": valor, "tipo": tipo, "categoria": categoria, "comentario": comentario, "data": str(data)})
        salvar_dados()
        st.success("Transação adicionada com sucesso")
        st.rerun()
    #adicionar transação

    #mostrar transações
    st.title("Transações registradas")

    st.dataframe(transacoes)

    data_inicial = st.date_input("data inicial")
    data_final = st.date_input("data final")

    if st.button("filtrar por período"):
        filtradas = filtrar_por_periodo(data_inicial, data_final)
        st.dataframe(filtradas)
        st.success("Transações filtradas por período")

    st.title("Gasto por categoria")

    totais = calcular_por_categoria()

    dados = {
        "categoria": list(totais.keys()),
        "valor": list(totais.values())
    }

    st.bar_chart(dados, x="categoria", y="valor")

    st.title("Gerenciar limites por categoria")


    nlimit_alimentacao = st.number_input("limite alimentação", value=limites["alimentação"], key="limite_alimentacao")
    nlimit_transporte = st.number_input("limite transporte", value=limites["transporte"], key="limite_transporte")
    nlimit_lazer = st.number_input("limite lazer", value=limites["lazer"], key="limite_lazer")
    nlimit_outros = st.number_input("limite outros", value=limites["outros"], key="limite_outros")

    if st.button("Salvar limites"):
        limites["alimentação"] = nlimit_alimentacao
        limites["transporte"] = nlimit_transporte
        limites["lazer"] = nlimit_lazer
        limites["outros"] = nlimit_outros
        salvar_limites()
        st.success("Limites atualizados com sucesso")
        st.rerun()

    for categoria in limites.keys():
        total_categoria = totais[categoria]
        limite_categoria = limites[categoria]
        limite_restante = limite_categoria - total_categoria

        st.progress(min(total_categoria / limite_categoria, 1), text=f"Gasto em {categoria}: R$ {total_categoria:.2f} / R$ {limite_categoria:.2f}")

        if total_categoria <= limite_categoria * 0.8:
            st.success(f"Você esta abaixo de 80% do limite de {categoria}! Limite restante: R$ {limite_restante:.2f}")
        elif total_categoria < limite_categoria:
            st.warning(f"Cuidado! Você esta acima de 80% do limite de {categoria}! Limite restante: R$ {limite_restante:.2f}")
        elif total_categoria >= limite_categoria:
            st.error(f"Atenção: gasto em {categoria} ultrapassou o limite definido!")

with aba2:
    st.title("Serviços em desenvolvimento")
    st.write("Estamos trabalhando em novas funcionalidades para melhorar sua experiência. Fique atento às atualizações futuras!")
#adicionar venda
    st.title("Adicionar venda")

    cliente = st.text_input("digite o nome do cliente:", key="cliente_servico")
    tipo = st.selectbox("qual o tipo do serviço?", ["Manutenção", "venda", "emprestimo"], key="tipo_servico")
    valor = st.number_input("digite o valor do serviço:", key="valor_servico")
    comentario = st.text_input("comentário (opcional)", key="comentario_servico")
    data = st.date_input("data", value=datetime.date.today(), key="data_servico")
    
    if st.button("adicionar", key="adicionar_servico"):
        adicionar_venda(cliente, tipo, valor, comentario, str(data))
        st.success("venda adicionada com sucesso")
        st.rerun()
#adicionar venda

#ver registros de vendas
    st.title("Vendas registradas")

    vendas = listar_vendas()
    df = pd.DataFrame(vendas, columns=["id", "cliente", "tipo", "valor_total", "comentario", "data"])

    st.dataframe(df)
#ver registros de vendas

#ver parcelas por cliente
    st.title("Consultar parcelas")

    nCliente = st.text_input("digite o nome do cliente para ver as parcelas:", key="cliente_parcelas")

    if st.button("listar parcelas", key="listar_parcelas_cliente"):
        ppc = listar_parcelas_por_cliente(nCliente)
        df_parcelas = pd.DataFrame(ppc, columns=["id", "venda_id", "valor", "status", "data"])
        st.dataframe(df_parcelas)

    st.write("Marcar como pago")
    parcela_id = st.number_input("Digite o ID da parcela para alterar o status:", key="parcela_id_status")

    if st.button("atualizar status", key="atualizar_status_parcela"):
        marcar_pago(parcela_id)
        st.success("Status da parcela atualizado com sucesso")
        st.rerun()
#ver parcelas por cliente

#adicionar parcelas e valor a venda
    st.title("Adicionar parcelas a venda")

    venda_id = st.number_input("digite o id da venda:", key="venda_id_parcelas")
    quantidade = st.selectbox("digite a quantidade de parcelas:", [1, 2, 3, 4, 5, 6], key="quantidade_parcelas")
    valor = st.number_input("digite o valor de cada parcela:", key="valor_parcela")
    status = st.selectbox("status da parcela:", ["pendente", "paga"], key="status_parcela")
    data = st.date_input("data", value=datetime.date.today(), key="data_parcela")

    if st.button("adicionar parcelas", key="adicionar_parcelas"):
        adicionar_parcela(venda_id, quantidade, valor, status, str(data))
        st.success("parcelas adicionadas com sucesso")
        st.rerun()