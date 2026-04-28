import json

#lista das transações, onde cada transação é um dicionário com as chaves "valor" e "tipo"
def carregar_dados():
    try:
        with open("transacoes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Erro ao carregar os dados. O arquivo está corrompido.")
        return []
    
def carregar_limites():
    try:
        with open("limites.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "alimentação": 1000,
            "transporte": 200,
            "lazer": 500,
            "outros": 1000
        }
    except json.JSONDecodeError:
        print("Erro ao carregar os dados. O arquivo está corrompido.")
        return {}

transacoes = carregar_dados()

limites = carregar_limites()



#streamlit
def salvar_dados():
    with open("transacoes.json", "w") as f:
        json.dump(transacoes, f)

def salvar_limites():
    with open("limites.json", "w") as f:
        json.dump(limites, f)

def calcular_por_categoria():
    totais_categoria = {
        "alimentação": 0,
        "transporte": 0,
        "lazer": 0,
        "outros": 0
    }

    for t in transacoes:
        if t["tipo"] == "saida":
            if t["categoria"] in totais_categoria:
                totais_categoria[t["categoria"]] += t["valor"]
    return totais_categoria


def imprimir_transacoes(lista):
    if not lista:
        print("nenhuma transação encontrada.")
        return
    for t in lista:
        print(f"valor: {t['valor']}, tipo: {t['tipo']}, categoria: {t['categoria']} comentário: {t.get('comentario', '')} data: {t.get('data', '')}")

def mostrar_transacoes():
    if not transacoes:
        print("nenhuma transação registrada.")
    else:
        print("transações registradas:")
        imprimir_transacoes(transacoes)

def calcular_resumo():
    saldo_entrada = 0
    saldo_saida = 0

    for t in transacoes:
        if t["tipo"] == "entrada":
                saldo_entrada += t["valor"]
        elif t["tipo"] == "saida":
                saldo_saida += t["valor"]

    saldo_total = saldo_entrada - saldo_saida

    return saldo_entrada, saldo_saida, saldo_total

def filtrar_por_tipo(opcao):
        
    filtradas = []


    for t in transacoes:
        if opcao == "1" and t["tipo"] == "entrada":
            filtradas.append(t)
        elif opcao == "2" and t["tipo"] == "saida":
            filtradas.append(t)
    
    if not filtradas:
        print("nenhuma transação encontrada para o tipo selecionado.")
        return
    imprimir_transacoes(filtradas)

def filtrar_por_categoria(opcao):

    filtradas = []

    for t in transacoes:
        if opcao == "1" and t["categoria"] == "alimentação":
            filtradas.append(t)
        elif opcao == "2" and t["categoria"] == "transporte":
            filtradas.append(t)
        elif opcao == "3" and t["categoria"] == "lazer":
            filtradas.append(t)
    if not filtradas:
        print("nenhuma transação encontrada para a categoria selecionada.")
        return
    imprimir_transacoes(filtradas)

def filtrar_por_periodo(data_inicial, data_final):

    filtradas = []

    for t in transacoes:
        if str(data_inicial) <= t.get("data", "") <= str(data_final):
            filtradas.append(t)

    if not filtradas:
        print("nenhuma transação encontrada para o período selecionado.")
    
    return filtradas


#opções para o usuário escolher o que deseja fazer