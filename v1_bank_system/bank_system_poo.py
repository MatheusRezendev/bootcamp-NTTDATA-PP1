from abc import ABC, abstractmethod
from datetime import datetime
import textwrap

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)
        
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, saldo, numero, agencia, cliente, historico=None):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico or Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):    
        saldo_inicial = 0.0
        agencia = "0001"
        return cls(saldo_inicial, numero, agencia, cliente)
        
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente    
    
    @property
    def historico(self):
        return self._historico
        
    def __str__(self):
        return f"\nAgência:\t{self.agencia}\nNúmero:\t\t{self.numero}\nTitular:\t{self.cliente.nome}\nSaldo:\t\tR$ {self.saldo:.2f}"

    def sacar(self, valor):
        if valor > self._saldo:
            print("\nFalhou! Você não tem saldo suficiente.")
        elif valor > 0:
            self._saldo -= valor
            transacao = Saque(valor)
            self.historico.adicionar_transacao(transacao)
            return True
        else:
            print("\nFalhou! Valor inválido.")
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            transacao = Deposito(valor)
            self.historico.adicionar_transacao(transacao)
            return True
        else:
            print("\nFalhou! Valor inválido.")
        return False

class ContaCorrente(Conta):
    def __init__(self, saldo, numero, cliente, agencia, limite=500, limite_saques=3):
        super().__init__(saldo, numero, agencia, cliente, Historico())
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len([t for t in self.historico.transacoes if t['tipo'] == 'Saque'])
        if valor > self.limite:
            print("Falhou! O valor excede o limite.")
        elif numero_saques >= self.limite_saques:
            print("Falhou! Limite de saques atingido.")
        elif valor > self.saldo:
            print("Falhou! Saldo insuficiente.")
        else:
            return super().sacar(valor)
        return False

    def __str__(self):
        return f"\nAgência:\t{self.agencia}\nNúmero:\t\t{self.numero}\nTitular:\t{self.cliente.nome}\nSaldo:\t\tR$ {self.saldo:.2f}\nLimite:\t\tR$ {self.limite:.2f}\nSaques:\t\t{self.limite_saques}"

class Historico:
    def __init__(self):
        self._transacoes = []
    
    @property    
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self.transacoes.append({'valor': transacao.valor, 'tipo': transacao.__class__.__name__})

class Transacao(ABC):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    @abstractmethod
    def registrar(self, conta: 'Conta'):
        pass

class Saque(Transacao):
    def registrar(self, conta):
        if conta.sacar(self._valor):
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def registrar(self, conta):
        if conta.depositar(self._valor):
            conta.historico.adicionar_transacao(self)

def menu():
    return input(
        """
        ================ MENU ================
        [d]\tDepositar
        [s]\tSacar
        [e]\tExtrato
        [nc]\tNova conta
        [lc]\tListar contas
        [nu]\tNovo usuário
        [q]\tSair
        => """
    )

def depositar(clientes):
    cpf = input("CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Valor do depósito: "))
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, Deposito(valor))

def sacar(clientes):
    cpf = input("CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    valor = float(input("Valor do saque: "))
    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    cliente.realizar_transacao(conta, Saque(valor))

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if len(clientes_filtrados) == 1 else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("Cliente sem contas cadastradas.")
        return
    return cliente.contas[0]

def exibir_extrato(clientes):
    cpf = input("CPF (somente números): ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("Cliente não encontrado.")
        return

    conta = recuperar_conta_cliente(cliente)

    if not conta:
        return

    print("\n========== EXTRATO ==========")
    transacoes = conta.historico.transacoes
    if not transacoes:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in transacoes:
            print(f"{transacao['tipo']}:\tR$ {transacao['valor']:.2f}")
    print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("==============================")

def criar_cliente(clientes):
    cpf = input("CPF (somente números): ")

    if filtrar_cliente(cpf, clientes):
        print("Cliente já existente.")
        return

    nome = input("Nome completo: ")
    data_nascimento = input("Data de nascimento (dd-mm-aaaa): ")
    endereco = input("Endereço: ")

    cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")

def criar_conta(numero_conta, clientes, contas):
    cpf = input("CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("CPF não encontrado.")
        return

    conta = ContaCorrente.nova_conta(cliente, numero_conta)
    contas.append(conta)
    cliente.adicionar_conta(conta)
    print(f"Conta criada com sucesso! Número: {conta.numero}")

def listar_contas(contas):
    for conta in contas:
        print("\n========== CONTA ==========")
        print(textwrap.dedent(str(conta)))

def main():
    clientes = []
    contas = []

    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)
        elif opcao == "s":
            sacar(clientes)
        elif opcao == "e":
            exibir_extrato(clientes)
        elif opcao == "nu":
            criar_cliente(clientes)
        elif opcao == "nc":
            criar_conta(len(contas) + 1, clientes, contas)
        elif opcao == "lc":
            listar_contas(contas)
        elif opcao == "q":
            print("Saindo... Obrigado por utilizar nosso sistema!")
            break
        else:
            print("\nOperação inválida.")

main()
