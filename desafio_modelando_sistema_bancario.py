import textwrap
from datetime import datetime
from abc import ABC, abstractclassmethod, abstractproperty


def menu():
    menu = """\n
    ================ MENU ================
    [1]\tNova conta
    [2]\tAcessar conta
    [3]\tConsultar conta
    [4]\tListar contas
    [5]\tSair
    => """
    return input(textwrap.dedent(menu))

def menu_cliente_opcoes():
    menu = """\n
    ================ MENU CLIENTE ================
    [1]\tConsultar saldo
    [2]\tRealizar saque
    [3]\tRealizar depósito
    [4]\tExibir extrato
    [5]\tVoltar ao menu principal
    => """
    return input(textwrap.dedent(menu))

def menu_cliente(conta):
    while True:
        opcao = menu_cliente_opcoes()
        if opcao == "1":
            print(f"\n=== Seu saldo atual é: R${conta.get_saldo:.2f} ===")
        elif opcao == "2":
            valor = float(input("Digite o valor a ser sacado: "))
            conta.sacar(valor) 
        elif opcao == "3":
            valor = float(input("Digite o valor a ser depositado: "))
            conta.depositar(valor)  
        elif opcao == "4":
            conta.historico.exibir_historico()  # Exibe o histórico de transações
        elif opcao == "5":
            print("\nVoltando ao menu principal...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self, conta, transacao):
        transacao.registrar = conta
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento
        
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def criar_conta(cls, numero, cliente):
        return cls(numero, cliente)

    @property
    def get_saldo(self):
        return self._saldo

    @property
    def get_numero(self):
        return self._numero

    @property
    def get_agencia(self):
        return self._agencia

    @property
    def get_cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def exibir_mensagem(self, sucesso, operacao):
        if sucesso:
            print(f"\n=== {operacao} realizado com sucesso! ===")
        else:
            print(f"\n@@@ Operação falhou! {operacao}. @@@")

    def sacar(self, valor):
        if valor > self._saldo:
            self.exibir_mensagem(False, "Você não tem saldo suficiente")
            return False
        elif valor <= 0:
            self.exibir_mensagem(False, "O valor informado é inválido")
            return False

        self._saldo -= valor
        self._historico.adicionar_transacao(Saque(valor))
        self.exibir_mensagem(True, "Saque")
        return True

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            self._historico.adicionar_transacao(Deposito(valor))
            self.exibir_mensagem(True, "Depósito")
            return True
        else:
            self.exibir_mensagem(False, "O valor informado é inválido")
            return False


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=3, limite_saque=500):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"]
        )

        excedeu_limite = valor > self.limite_saque
        excedeu_saques = numero_saques >= self.limite

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []  # Lista para armazenar as transações
    
    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
            }
        )

    def exibir_historico(self):
        print("\n================ Extrato ================")
        if not self._transacoes:
            print("Nenhuma transação realizada.")
        else:
            for transacao in self._transacoes:
                print(f"{transacao['data']} - {transacao['tipo']}: R${transacao['valor']:.2f}")
        print("===========================================")

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

class Banco:
    def __init__(self):
        self.clientes = []  # Lista para armazenar todos os clientes
        self.contas = []    # Lista para armazenar todas as contas

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def buscar_cliente_por_cpf(self, cpf):
        for cliente in self.clientes:
            if cliente.cpf == cpf:
                return cliente
        return None

    def buscar_conta_por_cpf(self, cpf):
        for conta in self.contas:
            cliente = conta.get_cliente  # Variável temporária
            if cliente.cpf == cpf:
                return conta
        return None

    def criar_conta(self):
        print("Criar nova conta")
        nome = input("Digite o nome do cliente: ")
        cpf = input("Digite o CPF do cliente: ")
        data_nascimento = input("Digite a data de nascimento do cliente (dd/mm/aaaa): ")
        endereco = input("Digite o endereço do cliente: ")

        # Verificar se o CPF já está cadastrado
        if self.buscar_cliente_por_cpf(cpf):
            print("\n@@@ CPF já cadastrado! Não é possível criar outra conta para este CPF. @@@")
            return

        # Criar cliente
        cliente = PessoaFisica(cpf, nome, data_nascimento, endereco)

        # Criar conta associada ao cliente
        numero_conta = len(self.contas) + 1
        conta = ContaCorrente.criar_conta(numero_conta, cliente)

        # Adicionar cliente e conta ao banco
        self.adicionar_cliente(cliente)
        self.adicionar_conta(conta)

        print(f"\n=== Conta criada com sucesso! ===")
        print(f"Agência: {conta.get_agencia}")
        print(f"Número da Conta: {conta.get_numero}")
        print(f"Titular: {cliente.nome}")


def main():
    banco = Banco()  # Instância do banco para gerenciar clientes e contas

    while True:
        opcao = menu()
        if opcao == "1":
            banco.criar_conta()
        elif opcao == "2":
            print("Acessar conta")
            cpf = input("Digite o CPF do cliente: ")
            conta = banco.buscar_conta_por_cpf(cpf)  # Busca a conta
            if conta:
                print(f"\n=== Acesso à conta de {conta.get_cliente.nome} ===")
                menu_cliente(conta)  # Passa a conta para o menu do cliente
            else:
                print("\n@@@ Conta não encontrada! @@@")
        elif opcao == "3":
            print("Consultar conta")
        elif opcao == "4":
            print("Listar contas")
        elif opcao == "5":
            print("Sair")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
# END

