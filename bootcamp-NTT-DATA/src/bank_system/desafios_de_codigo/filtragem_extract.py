def filtrar_visuais(lista_visuais):
    # Converter a string de entrada em uma lista
    entrada_usuario = list(map(str.strip, entrada_usuario.split(",")))
    
    visuais = lista_visuais.split(", ")
    
    # TODO: Normalize e remova duplicatas usando um conjunto
    
    entrada_usuario = set(visuals_usuario)
    
    # TODO: Realize a intersecção das duas listas
    
    lista_final = list(entrada_usuario.intersection(visuais))    
    
    # TODO: Converta o conjunto de volta para uma lista ordenada:
    
    lista_final.sort()    
    
    # Unir a lista em uma string, separada por vírgulas
    return ", ".join(lista_final)

# Capturar a entrada do usuário
entrada_usuario = input()

# Processar a entrada e obter a saída
saida = filtrar_visuais(entrada_usuario)
print(saida)