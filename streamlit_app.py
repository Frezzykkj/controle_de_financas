import streamlit as st
from app import carregar_dados, salvar_dados, transacoes, calcular_por_categoria, calcular_resumo

#resumo financeiro
st.title("Resumo Financeiro")

saldo_entrada, saldo_saida, saldo_total = calcular_resumo()

st.write(f"saldo total: R$ {saldo_total}")
st.write(f"Valor total de entradas: R$ {saldo_entrada}")
st.write(f"Valor total de saídas: R$ {saldo_saida}")

#resumo financeiro

#adicionar transação
st.title("Adicionar transação")

valor = st.number_input("digite o valor:")
tipo = st.selectbox("qual o tipo da transação?", ["entrada", "saida"])
categoria = st.selectbox("qual a categoria da transação?", ["alimentação", "transporte", "lazer", "trabalho", "outros"])

if st.button("adicionar"):
    transacoes.append({"valor": valor, "tipo": tipo, "categoria": categoria})
    salvar_dados()
    st.success("Transação adicionada com sucesso")
    st.rerun()
#adicionar transação

#mostrar transações
st.title("Transações registradas")

st.dataframe(transacoes)

st.write("resumo da transações:")

st.bar_chart({
    "Entradas": [saldo_entrada],
    "Saídas": [saldo_saida]
})

totais = calcular_por_categoria()

dados = {
      "categoria": list(totais.keys()),
      "valor": list(totais.values())
}

st.bar_chart(dados, x="categoria", y="valor")

