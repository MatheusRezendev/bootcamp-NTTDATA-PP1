menu = '''

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=> '''

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = int(input(menu))

    if(opcao == 1):
        valor_dep = float(input("Digite o valor que deseja depositar: "))
   
        if valor_dep > 0:
            saldo += valor_dep
            extrato += f"Deposito: R$ {valor_dep:.2f}\n"
            print("\n Deposito concluido com sucesso!")

        else:
            print("Operacao invalida. Digite um valor valido.")
        
    
    elif(opcao == 2):
        valor_saque = float(input("Digite o valor que deseja sacar: "))

        excedeu_saldo = valor_saque > saldo

        excedeu_saque = numero_saques >= LIMITE_SAQUES
        
        excedeu_limite = valor_saque > limite

        if excedeu_saldo:
            print("Falhou! Saldo insuficiente")
        elif excedeu_saque:
            print("Falhou! Limite de saques atingido")
        elif excedeu_limite:
            print("Falhou! O valor do saque excede o limite")
        elif valor_saque > 0:
            saldo -= valor_saque
            extrato += f"Saque: R$ {valor_saque:.2f}\n"
            numero_saques += 1
            print("\n Saque concluido com sucesso!")
        else:
            print("Nao foi possivel concluir operacao. O valor informado e invalido")
        
    elif(opcao == 3):
        print("\n###### EXTRATO ######")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("######################")

    
    elif(opcao == 0):
        print("Saindo...")
        break

    else:
        print("Operacao invalida, por favor selecione novamente!")


    