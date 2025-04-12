saldo = 2000 # Inicializa o saldo
saques_realizados = 0  # Variável global para contar o número de saques
Extrato = []  # Lista para armazenar os extratos

def menu():
    print("""
    ##### Bem-vindo ao sistema bancário! #####
                1. Consultar saldo
                2. Sacar
                3. Depositar
                4. Exibir extrato
                5. Sair
    ##########################################
    """)
    try:
        opcao = int(input("Escolha uma opção: "))
        return opcao
    except ValueError:
        print("Opção inválida! Por favor, digite um número.")
        return 0

def consultar_saldo():
    global saldo
    print(f"Seu saldo atual é R$ {saldo:.2f}")

    voltar = input("Deseja realizar outra operação? (s/n): ").lower()
    if voltar != 's':
        print("Saindo do sistema bancário. Até logo!")
        exit()  # Encerra o programa se o usuário não quiser continuar

# Função para sacar dinheiro
def sacar():
    global saldo
    global saques_realizados
    global Extrato

    if saques_realizados >= 3:
        print("Limite de saques atingido. Tente novamente amanhã.\n\n")
        return

    while True:  # Loop para garantir que o usuário insira um valor válido
        try:
            valor = float(input("\nDigite o valor a ser sacado: "))
            if valor <= 0:
                print("Valor inválido. Tente novamente.\n\n")
            elif valor > saldo:
                print("Saldo insuficiente.\n\n")
            elif valor > 500:
                print("Valor máximo para saque é de R$ 500,00.\n\n")
            else:
                saldo -= valor
                saques_realizados += 1  # Incrementa o contador de saques
                Extrato.append(f"Saque de R$ {valor:.2f}")  # Adiciona ao extrato
                print(f"Saque de R$ {valor:.2f} realizado com sucesso.\n\n")
                break  # Sai do loop após um saque bem-sucedido
        except ValueError:
            print("Entrada inválida! Por favor, digite um número válido.\n\n")

    voltar = input("Deseja realizar outra operação? (s/n): ").lower()
    if voltar != 's':
        print("Saindo do sistema bancário. Até logo!")
        exit()  # Encerra o programa se o usuário não quiser continuar 

# Função para depositar dinheiro
def depositar():
    global saldo
    global Extrato

    valor = float(input("\nDigite o valor a ser depositado: "))
    if valor > 0:
        saldo += valor
        Extrato.append(f"Depósito de R$ {valor:.2f}")  # Adiciona ao extrato
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.\n\n")
    else:
        print("Valor de depósito inválido. Tente novamente.\n\n")
    voltar = input("Deseja realizar outra operação? (s/n): ").lower()
    if voltar != 's':
        print("Saindo do sistema bancário. Até logo!")
        exit()  # Encerra o programa se o usuário não quiser continuar 

# Função para exibir o extrato
def exibir_extrato():
    global Extrato
    global saldo

    print("\n##### Extrato Bancário #####")
    if len(Extrato) == 0:
        print("Nenhuma transação realizada.")
    else:
        for transacao in Extrato:
            print(transacao)
    print(f"\nSaldo atual: R$ {saldo:.2f}")
    print("############################\n")
    voltar = input("Deseja realizar outra operação? (s/n): ").lower()
    if voltar != 's':
        print("Saindo do sistema bancário. Até logo!")
        exit()  # Encerra o programa se o usuário não quiser continuar 

# Início do programa
if __name__ == "__main__":
    while True:
        opcao = menu()
        if opcao == 1:
            consultar_saldo()
        elif opcao == 2:
            sacar()
        elif opcao == 3:
            depositar()
        elif opcao == 4:
            exibir_extrato()  # Chama a função para exibir o extrato
        elif opcao == 5:
            print("Saindo do sistema bancário. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

