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

transacoes = carregar_dados()



#streamlit
def salvar_dados():
    with open("transacoes.json", "w") as f:
        json.dump(transacoes, f)

def calcular_por_categoria():
    totais_categoria = {
        "alimentação": 0,
        "transporte": 0,
        "lazer": 0,
        "trabalho": 0,
        "outros": 0
    }

    for t in transacoes:
        if t["categoria"] in totais_categoria:
            totais_categoria[t["categoria"]] += t["valor"]
    return totais_categoria


def imprimir_transacoes(lista):
    if not lista:
        print("nenhuma transação encontrada.")
        return
    for t in lista:
        print(f"valor: {t['valor']}, tipo: {t['tipo']}, categoria: {t['categoria']}")

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


#terminal 
def adicionar_transacao():
        valor = float(input("digite o valor da transação: "))

        print("qual o tipo da transação?")
        print("1. entrada")
        print("2. saida")

        opcao = (input("digite a opção (1 ou 2): "))
        if opcao == "1":
            tipo = "entrada"
        elif opcao == "2":
            tipo = "saida"
        else:
            print("opção inválida. A transação não será adicionada.")
            return
        
        print("qual a categoria da transação?")
        print("1. alimentação")
        print("2. transporte")
        print("3. lazer")
        print("4. trabalho")

        categoria_opcao = input("digite a opção (1, 2, 3 ou 4): ")

        if categoria_opcao == "1":
            categoria = "alimentação"
        elif categoria_opcao == "2":
            categoria = "transporte"
        elif categoria_opcao == "3":
            categoria = "lazer"
        elif categoria_opcao == "4":
            categoria = "trabalho"
        else:            
            print("opção inválida. A transação não será adicionada.")
            return
        
        
        transacoes.append({"valor": valor, "tipo": tipo, "categoria": categoria})
        salvar_dados()

def filtrar_por_tipo():
    print("qual tipo de transação deseja filtrar?")
    print("1. entrada")
    print("2. saida")
    opcao = input("digite a opção (1 ou 2): ")

    if opcao not in ["1", "2"]:
        print("opção inválida. Por favor, tente novamente.")
        return
    
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

def filtrar_por_categoria():
    print("qual categoria de transação deseja filtrar?")
    print("1. alimentação")
    print("2. transporte")
    print("3. lazer")
    print("4. trabalho")
    opcao = input("digite a opção (1, 2, 3 ou 4): ")
    
    if opcao not in ["1", "2", "3", "4"]:
        print("opção inválida. Por favor, tente novamente.")
        return
    
    filtradas = []

    for t in transacoes:
        if opcao == "1" and t["categoria"] == "alimentação":
            filtradas.append(t)
        elif opcao == "2" and t["categoria"] == "transporte":
            filtradas.append(t)
        elif opcao == "3" and t["categoria"] == "lazer":
            filtradas.append(t)
        elif opcao == "4" and t["categoria"] == "trabalho":
            filtradas.append(t)
    if not filtradas:
        print("nenhuma transação encontrada para a categoria selecionada.")
        return
    imprimir_transacoes(filtradas)

#opções para o usuário escolher o que deseja fazer
if __name__ == "__main__":
    while True:

        print("selecione uma opção:")
        print("1. adicionar transação")
        print("2. mostrar transações")
        print("3. calcular resumo")
        print("4. filtrar por tipo")
        print("5. filtrar por categoria")

        input_usuario = input("digite a opção (1, 2, 3, 4 ou 5): ")

        if input_usuario == "1":
            adicionar_transacao()
        elif input_usuario == "2":
            mostrar_transacoes()
        elif input_usuario == "3":
            calcular_resumo()
        elif input_usuario == "4":
            filtrar_por_tipo()
        elif input_usuario == "5":
            filtrar_por_categoria()
        else:
            print("opção inválida. Por favor, tente novamente.")