from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001" 
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
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
    
    def sacar(self, valor):
        saldo = self._saldo
        excedeu_saldo = valor > saldo
        if excedeu_saldo:
            print("\n*** Operacao falhou! Saldo insuficiente.")
        
        elif valor > 0:
            self._saldo -= valor
            print("\n+++ Saque realizado com sucesso!")
            return True
        
        else:
            print("\n*** Operacao Falhou! valor invalido.")
        
        return False
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n+++ Deposito realizado com sucesso!")
        
        else:
            print("\n*** Operacao Falhou! valor invalido.")
            return False
    
        return True

    


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.
            transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques

        if excedeu_limite:
            print("\n*** Operacao Falhou! valor excedeu limite.")
        
        elif excedeu_saques:
            print("\n*** Operacao Falhou! excedeu numero de saques.")
        
        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""
            Agencia:\t{self.agencia}
            C/C:\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._trancacoes = []
    
    @property
    def transacoes(self):
        return self._trancacoes
    
    def adicionar_transaceo(self, transacao):
        self._trancacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
        )

class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass
    
    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)        


def show_menu():
    menu = """
    ====== Menu iBanco ======
    [d]  Depósito
    [s]  Saque
    [e]  Extrato
    [nc] Criar conta
    [lc] Listar conta
    [nu] Novo usuário
    [q]  Sair
    => """
    return input(menu)


def filtrar_clientes(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("** Cliente nao possui conta!")
        return
    
    return cliente.contas[0]


def depositar(clientes):
    cpf = input("Informe CPF")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print('** Cliente nao encontrado!')
        return 
    
    valor = float(input("Informe o valor:"))
    transacao = Deposito(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe CPF")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print('** Cliente nao encontrado!')
        return 
    
    valor = float(input("Informe o valor:"))
    transacao = Saque(valor)
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe CPF")
    cliente = filtrar_clientes(cpf, clientes)

    if not cliente:
        print('** Cliente nao encontrado!')
        return 

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print('----------------- EXTRATO --------------')
    transacoes = conta.historico.transacoes
    extrato = ''
    if not transacoes:
        extrato = 'Nao foram realizadas transacoes'
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR${transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("-----------------------------------------")


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe CPF")
    cliente = filtrar_clientes(cpf, clientes)
    if not cliente:
        print('** Cliente nao encontrado!')
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print('\n --- Conta criada com sucesso!')


def criar_cliente(clientes):
    cpf = input("Informe CPF:")
    cliente = filtrar_clientes(cpf, clientes)
    if cliente:
        print('** Cliente ja existe!')
        return
    nome = input("Informe nome completo:")
    data_nascimento = input("Informe data de nascimento (dd-mm-aaaa):")
    endereco = input("Informe endereco:")
  
    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento,
                           cpf=cpf, endereco=endereco)
    
    clientes.append(cliente)

    print('--- Cliente criado com sucesso!')


def listar_contas(contas):
    for conta in contas:
        print('=' * 80)
        print(str(conta))


if __name__ == "__main__":
    clientes = []
    contas = []

    while True:
        opcao = show_menu()

        if opcao == 'd':
            depositar(clientes)

        elif opcao == 's':
            sacar(clientes)
        
        elif opcao == 'e':
            exibir_extrato(clientes)
        
        elif opcao == 'nu':
            criar_cliente(clientes)
        
        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)
        
        elif opcao == 'lc':
            listar_contas(contas)
        
        elif opcao == 'q':
            break

        else:
            print('** Opção inválida!')
