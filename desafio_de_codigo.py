def analise_vendas(vendas):
    total_vendas = 0
   
    for venda in vendas:
        total_vendas += venda
        
    media_vendas = total_vendas / len(vendas) if vendas else 0
    # TODO: Calcule o total de vendas e realize a média mensal:
    
    return f"{total_vendas}, {media_vendas:.2f}"

def obter_entrada_vendas():
    
    # Solicita a entrada do usuário em uma única linha
    entrada = str(input("Digite o valor das vendas (separando por virgula): "))
    
    # TODO: Converta a entrada em uma lista de inteiros:
    split_string = entrada.split(",")
   
    entrada = list(map(int, split_string))  

    vendas = entrada
    return vendas

vendas = obter_entrada_vendas()
print(analise_vendas(vendas))