import streamlit as st
from app import carregar_dados, salvar_dados, transacoes, calcular_por_categoria, calcular_resumo, limites, salvar_limites

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
if tipo == "entrada":
    categoria = None
elif tipo == "saida":
    categoria = st.selectbox("qual a categoria da transação?", ["alimentação", "transporte", "lazer", "outros"])
comentario = st.text_input("comentário (opcional)")

if st.button("adicionar"):
    transacoes.append({"valor": valor, "tipo": tipo, "categoria": categoria, "comentario": comentario})
    salvar_dados()
    st.success("Transação adicionada com sucesso")
    st.rerun()
#adicionar transação

#mostrar transações
st.title("Transações registradas")

st.dataframe(transacoes)

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


total_alimentacao = totais["alimentação"]
total_transporte = totais["transporte"]
total_lazer = totais["lazer"]
total_outros = totais["outros"]

for categoria in limites.keys():
    total_categoria = totais[categoria]
    limite_categoria = limites[categoria]
    limite_restante = limite_categoria - total_categoria

    st.progress(total_categoria / limite_categoria, text=f"Gasto em {categoria}: R$ {total_categoria:.2f} / R$ {limite_categoria:.2f}")

    if total_categoria <= limite_categoria * 0.8:
        st.success(f"Você esta abaixo de 80% do limite de {categoria}! Limite restante: R$ {limite_restante:.2f}")
    elif total_categoria < limite_categoria:
        st.warning(f"Cuidado! Você esta acima de 80% do limite de {categoria}! Limite restante: R$ {limite_restante:.2f}")
    elif total_categoria >= limite_categoria:
        st.error(f"Atenção: gasto em {categoria} ultrapassou o limite definido!")

