import json

#carregamento e salvamento de dados
def carregar_dados():
    try:
        with open("storage/transacoes.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []
    
def carregar_limites():
    try:
        with open("storage/limites.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "alimentação": 1000,
            "transporte": 200,
            "lazer": 500,
            "outros": 1000
        }
    except json.JSONDecodeError:
        return {}
#carregamento e salvamento de dados

transacoes = carregar_dados()

limites = carregar_limites()

#streamlit
def salvar_dados():
    with open("storage/transacoes.json", "w") as f:
        json.dump(transacoes, f)

def salvar_limites():
    with open("storage/limites.json", "w") as f:
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

def filtrar_por_periodo(data_inicial, data_final):

    filtradas = []

    for t in transacoes:
        if str(data_inicial) <= t.get("data", "") <= str(data_final):
            filtradas.append(t)

    return filtradas