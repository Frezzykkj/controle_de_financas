import json

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