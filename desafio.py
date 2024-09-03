
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


def depositar(saldo, valor, extrato, /):

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print('++ Depósito efetuado com sucesso!')
    else:
        print("** Operação falhou! O valor informado é inválido. **")
    
    return saldo, extrato


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    
    if valor > saldo:
        print("** Operação falhou! Você não tem saldo suficiente!")

    elif valor > limite:
        print("** Operação falhou! O valor do saque excede o limite!")

    elif numero_saques >= limite_saques:
        print("** Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("-- Saque efetuado com sucesso!")
    else:
        print("** Operação falhou! O valor informado é inválido.")
        
    return saldo, extrato, numero_saques


def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")
    

def criar_usuario(usuarios):
    cpf = input('Informe CPF (apenas numeros): ')
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('** CPF já cadastrado!')
        return
    
    nome = input('Nome completo: ')
    data_nascimento = input('Data de nascimento (dd-mm-aaaa): ')
    endereco = input('Endereço (rua, número, bairro, cidade/UF): ')

    usuarios.append({'nome': nome, 'data_nascimento': data_nascimento,
                      'cpf': cpf, 'endereco': endereco})
    
    print("++ Usuário cadastrado com sucesso!")


def filtrar_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario['cpf'] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None
    

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe CPF: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print('++ Conta Criada!')
        return {'agencia': agencia, 'numero_conta': numero_conta, 'usuario': usuario }
    
    print('** Usuário não encontrado, processo finalizado!')


def listar_contas(contas):
    for conta in contas:
        linha = f"""
            Agência: {conta['agencia']}
            C/C.: {conta['numero_conta']}
            Titular: {conta['usuario']['nome']}
        """
        print('-' * 70)
        print(linha)


if __name__ == '__main__':
    AGENCIA = '0001'
    LIMITE = 500
    LIMITE_SAQUES = 3

    saldo = 0
    extrato = ""
    numero_saques = 0
    contas = []
    usuarios = []

    while True:
        opcao = show_menu()

        if opcao == 'd':
            valor = float(input("Valor do depósito: "))

            saldo, extrato = depositar(saldo, valor, extrato)

        elif opcao == 's':
            valor = float(input('Valor do saque: '))

            saldo, extrato, numero_saques = sacar(saldo=saldo, valor=valor,
                                                  extrato=extrato, limite=LIMITE,
                                                  numero_saques=numero_saques,
                                                  limite_saques=LIMITE_SAQUES)
        
        elif opcao == 'e':
            exibir_extrato(saldo, extrato=extrato)
        
        elif opcao == 'nu':
            criar_usuario(usuarios)
        
        elif opcao == 'nc':
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
        
        elif opcao == 'lc':
            listar_contas(contas)
        
        elif opcao == 'q':
            break

        else:
            print('** Opção inválida!')


