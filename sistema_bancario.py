from datetime import datetime
from getpass import getpass

LIMITE_TRANSACOES = 10
LIMITE_SAQUES = 3
LIMITE_VALOR_SAQUE = 500
MENSAGEM_SALDO_INSUFICIENTE = "Saldo insuficiente para saque."
MENSAGEM_LIMITE_SAQUES = "Limite de saques diários atingido. Tente novamente amanhã."

class SistemaBancario:
    def __init__(self):
        self.clientes = {}
        self.contas = {}
        self.proximo_numero_conta = 1000

    def cadastrar_cliente(self):
        # Lógica de cadastro de cliente
        pass

    def criar_conta(self, cpf):
        # Lógica de criação de conta
        pass

    def consultar_saldo(self, cpf):
        # Lógica de consulta de saldo
        pass

    def menu_inicial(self):
        while True:
            opcao = exibir_menu([
                "Acessar como Funcionário",
                "Acessar como Cliente",
                "Sair"
            ])
            if opcao == 1:
                senha_funcionario = getpass("Digite a senha do funcionário: ")
                if senha_funcionario != "1234":
                    print("Senha incorreta! Tente novamente.")
                    continue
                print("Acesso autorizado!")
                menu_funcionario()  # Redireciona para o menu do funcionário
            elif opcao == 2:
                cpf_cliente = input("Digite seu CPF: ")
                if cpf_cliente not in clientes:
                    print("Cliente não encontrado.")
                    continue
                senha_cliente = getpass("Digite sua senha: ")
                if senha_cliente != "1234":
                    print("Senha incorreta! Tente novamente.")
                    continue
                print(f"Bem-vindo, {clientes[cpf_cliente].nome}!")
                while True:
                    opcao_cliente = menu()
                    if opcao_cliente == 1:
                        consultar_saldo(cpf_cliente)  # Passa o CPF como argumento
                    elif opcao_cliente == 2:
                        sacar(cpf_cliente)  # Passa o CPF como argumento
                    elif opcao_cliente == 3:
                        depositar(cpf_cliente)  # Passa o CPF como argumento
                    elif opcao_cliente == 4:
                        exibir_extrato(cpf_cliente)  # Passa o CPF como argumento
                    elif opcao_cliente == 5:
                        print("Saindo do sistema bancário. Até logo!")
                        break
                    else:
                        print("Opção inválida! Tente novamente.")
            elif opcao == 3:
                print("Saindo do sistema bancário. Até logo!")
                exit()  # Encerra o programa
            else:
                print("Opção inválida! Tente novamente.")

clientes = {}   # Dicionário para armazenar os clientes (CPF como chave e objeto Cliente como valor)
contas = {}  # Dicionário para armazenar as contas (CPF como chave e informações da conta como valor)
proximo_numero_conta = 1000  # Variável global para gerar números de conta únicos

class Cliente:
    def __init__(self):
        self.nome = ""
        self.data_nascimento = 0
        self.cpf = ""
        self.endereco = ""  # Armazena o endereço completo como uma única string
        self.conta = None  # Inicializa a conta como None

def cadastrar_cliente():
    cliente = Cliente()
    cliente.nome = input("Digite o nome do cliente: ")
    cliente.data_nascimento = input("Digite a data de nascimento (DD/MM/AAAA): ")

    while True:
        cliente.cpf = input("Digite o CPF (apenas números): ")
        if validar_cpf(cliente.cpf):
            break  # Sai do loop se o CPF for válido

    # Solicita o endereço completo
    cliente.endereco = input("Digite o endereço no formato 'Logradouro, nro - Bairro - Cidade/Sigla estado': ")

    if cliente.cpf in clientes:
        print("Já existe um cliente cadastrado com este CPF.")
    else:
        clientes[cliente.cpf] = cliente  # Adiciona o cliente ao dicionário
        print(f"Cliente {cliente.nome} cadastrado com sucesso!")
    return cliente

def validar_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit():
        print("CPF inválido! Certifique-se de que o CPF contém 11 números.")
        return False
    return True

def consultar_cliente():
    while True:
        cpf = input("Digite o CPF do cliente que deseja consultar (apenas números): ")
        if validar_cpf(cpf):
            break  # Sai do loop se o CPF for válido

    if cpf in clientes:
        cliente = clientes[cpf]
        print(f"Nome: {cliente.nome}")
        print(f"Data de Nascimento: {cliente.data_nascimento}")
        print(f"CPF: {cliente.cpf}")
        print(f"Endereço: {cliente.endereco}")  # Exibe o endereço completo
    else:
        print("Cliente não encontrado.")

def gerar_numero_conta():
    global proximo_numero_conta
    numero_conta = proximo_numero_conta
    proximo_numero_conta += 1
    return numero_conta

def criar_conta():
    while True:
        cpf = input("Digite o CPF do cliente para criar a conta (apenas números): ")
        if validar_cpf(cpf):
            break  # Sai do loop se o CPF for válido

    if cpf in clientes:
        if cpf in contas:
            print(f"O cliente já possui uma conta. Agência: 0001, Número da conta: {contas[cpf]['numero_conta']}")
        else:
            numero_conta = gerar_numero_conta()
            contas[cpf] = {
                "agencia": "0001",
                "numero_conta": numero_conta,
                "saldo": 0,  # Saldo inicial
                "extrato": [],  # Lista para armazenar o extrato individual
                "saques_diarios": 0,  # Contador de saques diários
                "operacoes_diarias": 0,  # Contador de operações diárias
                "data_ultima_operacao": datetime.now().strftime('%d/%m/%Y')  # Data da última operação
            }
            print(f"Conta criada com sucesso! Agência: 0001, Número da conta: {numero_conta}")
    else:
        print("CPF não encontrado. Cadastre o cliente antes de criar uma conta.")

def consultar_conta():
    cpf = input("Digite o CPF do cliente para consultar a conta: ")
    if cpf in contas:
        print(f"O cliente possui a conta na Agência: {contas[cpf]['agencia']}, Número da conta: {contas[cpf]['numero_conta']}")
    else:
        print("Conta não encontrada para este CPF.")

def exibir_menu(opcoes):
    print("\n##### Menu #####")
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i}. {opcao}")
    print("################")
    try:
        return int(input("Escolha uma opção: "))
    except ValueError:
        print("Entrada inválida! Por favor, digite um número.")
        return 0

def menu_funcionario():
    while True:
        opcao = exibir_menu(["Cadastrar cliente", "Consultar cliente", "Criar conta", "Consultar conta", "Sair"])
        if opcao == 1:
            cadastrar_cliente()
        elif opcao == 2:
            consultar_cliente()
        elif opcao == 3:
            criar_conta()
        elif opcao == 4:
            consultar_conta()
        elif opcao == 5:
            print("Saindo do sistema bancário. Até logo!")
            break
        else:
            print("Opção inválida! Tente novamente.")

def verificar_limite_transacoes():
    global transacoes_diarias
    if transacoes_diarias >= LIMITE_TRANSACOES:
        print("Limite de transações diárias atingido. Tente novamente amanhã.")
        exit()

def verificar_e_reiniciar_contadores(cpf):
    data_atual = datetime.now().strftime('%d/%m/%Y')
    if contas[cpf]["data_ultima_operacao"] != data_atual:
        contas[cpf]["saques_diarios"] = 0
        contas[cpf]["operacoes_diarias"] = 0
        contas[cpf]["data_ultima_operacao"] = data_atual

def verificar_conta(cpf):
    if cpf not in contas:
        print("Conta não encontrada para este CPF.")
        return False
    return True

def voltar_ao_menu():
    voltar = input("Deseja realizar outra operação? (s/n): ").lower()
    if voltar != 's':
        print("Saindo do sistema bancário. Até logo!")
        menu_inicial()  # Redireciona para o menu inicial

def obter_valor(mensagem):
    while True:
        try:
            valor = float(input(mensagem))
            if valor > 0:
                return valor
            else:
                print("O valor deve ser positivo. Tente novamente.")
        except ValueError:
            print("Entrada inválida! Por favor, digite um número válido.")

def menu():
    opcao = exibir_menu([
        "Consultar saldo",
        "Sacar",
        "Depositar",
        "Exibir extrato",
        "Sair"
    ])
    return opcao

def consultar_saldo(cpf):
    if not verificar_conta(cpf):
        return
    saldo = contas[cpf]["saldo"]
    print(f"Seu saldo atual é R$ {saldo:.2f}")

def sacar(cpf):
    if cpf in contas:
        verificar_e_reiniciar_contadores(cpf)  # Verifica e reinicia os contadores, se necessário

        if contas[cpf]["operacoes_diarias"] >= LIMITE_TRANSACOES:
            print("Limite de operações diárias atingido. Tente novamente amanhã.")
            return

        if contas[cpf]["saques_diarios"] >= LIMITE_SAQUES:
            print(MENSAGEM_LIMITE_SAQUES)
            return

        if contas[cpf]["saldo"] <= 0:
            print(MENSAGEM_SALDO_INSUFICIENTE)
            return

        while True:
            valor = obter_valor("Digite o valor a ser sacado: ")
            if valor > contas[cpf]["saldo"]:
                print("Saldo insuficiente.")
            elif valor > LIMITE_VALOR_SAQUE:
                print(f"Valor máximo para saque é de R$ {LIMITE_VALOR_SAQUE:.2f}.")
            else:
                contas[cpf]["saldo"] -= valor
                contas[cpf]["extrato"].append(f"Saque de R$ {valor:.2f} em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
                contas[cpf]["saques_diarios"] += 1  # Incrementa o contador de saques
                contas[cpf]["operacoes_diarias"] += 1  # Incrementa o contador de operações
                print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
                break
    else:
        print("Conta não encontrada para este CPF.")

def depositar(cpf):
    if cpf in contas:
        verificar_e_reiniciar_contadores(cpf)  # Verifica e reinicia os contadores, se necessário

        if contas[cpf]["operacoes_diarias"] >= LIMITE_TRANSACOES:
            print("Limite de operações diárias atingido. Tente novamente amanhã.")
            return

        valor = obter_valor("Digite o valor a ser depositado: ")
        contas[cpf]["saldo"] += valor
        contas[cpf]["extrato"].append(f"Depósito de R$ {valor:.2f} em {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        contas[cpf]["operacoes_diarias"] += 1  # Incrementa o contador de operações
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
    else:
        print("Conta não encontrada para este CPF.")

def exibir_extrato(cpf):
    if cpf in contas:
        verificar_e_reiniciar_contadores(cpf)  # Verifica e reinicia os contadores, se necessário

        print("\n##### Extrato Bancário #####")
        if len(contas[cpf]["extrato"]) == 0:
            print("Nenhuma transação realizada.")
        else:
            for transacao in contas[cpf]["extrato"]:
                print(transacao)
        saldo = contas[cpf]["saldo"]
        print(f"\nSaldo atual: R$ {saldo:.2f}")
        print(f"Operações realizadas hoje: {contas[cpf]['operacoes_diarias']}")
        print("############################\n")
    else:
        print("Conta não encontrada para este CPF.")

# Início do programa
if __name__ == "__main__":
    sistema = SistemaBancario()
    sistema.menu_inicial()


