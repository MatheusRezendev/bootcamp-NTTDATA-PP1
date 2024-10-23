import textwrap

def menu():
    menu = '''
    ================ MENU ================
    
    [nu] Novo usuario
    [nc] Nova conta
    [l] Listar contas
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [q] Sair

    ======================================
    => '''
    
    return input(textwrap.dedent(menu))

def depositar(conta, valor_dep):
    if valor_dep > 0:
        conta['saldo'] += valor_dep
        conta['extrato'] += f"Deposito: R$ {valor_dep:.2f}\n"
        print("\nDeposito concluido com sucesso!")
    else:
        print("Operacao invalida. Digite um valor valido.")

def sacar(conta, valor_saque, limite, numero_saques, LIMITE_SAQUES):
    excedeu_saldo = valor_saque > conta['saldo']
    excedeu_saque = numero_saques >= LIMITE_SAQUES
    excedeu_limite = valor_saque > limite

    if excedeu_saldo:
        print("Falhou! Saldo insuficiente")
    elif excedeu_saque:
        print("Falhou! Limite de saques atingido")
    elif excedeu_limite:
        print("Falhou! O valor do saque excede o limite")
    elif valor_saque > 0:
        conta['saldo'] -= valor_saque
        conta['extrato'] += f"Saque: R$ {valor_saque:.2f}\n"
        numero_saques += 1
        print("\nSaque concluido com sucesso!")
    else:
        print("Nao foi possivel concluir operacao. O valor informado e invalido")

    return numero_saques

def exibir_extrato(conta):
    print("\n###### EXTRATO ######")
    print("Não foram realizadas movimentações." if not conta['extrato'] else conta['extrato'])
    print(f"\nSaldo: R$ {conta['saldo']:.2f}")
    print("######################")

def criar_conta(agencia, numero_conta, usuario):
    return {
        "agencia": agencia,
        "numero": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": ""
    }

def criar_usuario(usuarios):
    cpf = input("Informe o CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)
    
    if usuario:
        print("\nJá existe um usuário com esse CPF!")
        return None

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf})
    print("\nUsuário criado com sucesso!")
    return usuarios[-1]  

def filtrar_usuario(cpf, usuarios):  
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def listar_contas(contas):
    print("\nContas:")
    for conta in contas:
        print(textwrap.dedent(str(conta)))

def main():
    LIMITE_SAQUES = 3
    AGENCIA = "0001"
    
    usuarios = []
    contas = []
    
    while True:
        opcao = menu()

        if opcao == "d":
            cpf = input("Informe o CPF do usuário: ")
            usuario = filtrar_usuario(cpf, usuarios)
            conta = next((c for c in contas if c['usuario']['cpf'] == cpf), None)

            if conta:
                valor_dep = float(input("Digite o valor que deseja depositar: "))
                depositar(conta, valor_dep)
            else:
                print("Usuário ou conta não encontrada.")
            
        elif opcao == "s":
            cpf = input("Informe o CPF do usuário: ")
            conta = next((c for c in contas if c['usuario']['cpf'] == cpf), None)

            if conta:
                valor_saque = float(input("Digite o valor que deseja sacar: "))
                numero_saques = sacar(conta, valor_saque, 500, 0, LIMITE_SAQUES)
            else:
                print("Usuário ou conta não encontrada.")
    
        elif opcao == "e":
            cpf = input("Informe o CPF do usuário: ")
            conta = next((c for c in contas if c['usuario']['cpf'] == cpf), None)

            if conta:
                exibir_extrato(conta)
            else:
                print("Usuário ou conta não encontrada.")
            
        elif opcao == "nu":
            usuario = criar_usuario(usuarios)
        
        elif opcao == "nc":
            usuario_cpf = input("Informe o CPF do usuário: ")
            usuario = filtrar_usuario(usuario_cpf, usuarios)

            if usuario:
                numero_conta = len(contas) + 1
                conta = criar_conta(AGENCIA, numero_conta, usuario)
                contas.append(conta)
                print("\nConta criada com sucesso!")
            else:
                print("\nUsuário não encontrado, não foi possível criar a conta.")
        
        elif opcao == "l":
            listar_contas(contas)
   
        elif opcao == "q":
            print("Saindo...")
            break

        else:
            print("Operacao invalida, por favor selecione novamente!")
    
main()
