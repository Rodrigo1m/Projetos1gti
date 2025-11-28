usuarios = {}

def carregar_usuarios():
    try:
        with open("usuarios.txt", "r", encoding="utf-8") as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                if linha:
                    email, nome, senha = linha.split(";")
                    usuarios[email] = {"nome": nome, "senha": senha}
    except FileNotFoundError:
        pass

def salvar_usuarios():
    with open("usuarios.txt", "w", encoding="utf-8") as arquivo:
        for email, dados in usuarios.items():
            arquivo.write(f"{email};{dados['nome']};{dados['senha']}\n")

def menu_principal():
    print("\nMENU PRINCIPAL")
    print("1 - Cadastrar usuária")
    print("2 - Login")
    print("3 - Ver Notícias")
    opcao = input("Escolha uma opção: ")
    return opcao

def cadastrar_usuario():
    print("\nCADASTRO DE USUÁRIA")
    nome = input("Nome: ")
    email = input("E-mail: ")
    senha = input("Senha: ")

    if email in usuarios:
        print("E-mail já cadastrado!")
    else:
        usuarios[email] = {"nome": nome, "senha": senha}
        salvar_usuarios()
        print("Usuária criada com sucesso!")

def login():
    print("\nLOGIN")
    email = input("E-mail: ")
    senha = input("Senha: ")

    if email in usuarios and usuarios[email]["senha"] == senha:
        print("Login bem-sucedido!")
        painel_usuaria(email)
    else:
        print("E-mail ou senha incorretos.")

def ver_noticias():
    print("\nNOTÍCIAS")
    print("1. Projeto Conecta Girl promove mentoria para jovens mulheres.")
    print("2. Novas bolsas de estudo disponíveis para tecnologia.")
    print("3. Evento online: Mulheres na Ciência e Inovação.")
    input("\nPressione ENTER para retornar ao menu principal.")

def painel_usuaria(email):
    while True:
        print(f"\nPAINEL DA USUÁRIA ({usuarios[email]['nome']})")
        print("1 - Ver oportunidades")
        print("2 - Apoio psicopedagógico")
        print("3 - Editar perfil")
        print("4 - Logout")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            ver_oportunidades()
        elif opcao == "2":
            apoio_psicopedagogico()
        elif opcao == "3":
            editar_perfil(email)
        elif opcao == "4":
            print("Sessão encerrada. Retornando ao menu principal")
            break
        else:
            print("Opção inválida!")

def ver_oportunidades():
    print("\nOPORTUNIDADES")
    print("1. Estágio em Tecnologia - Empresa Tech4Girls")
    print("2. Bolsa de estudos em Programação - Instituto Mulheres Digitais")
    print("3. Mentoria gratuita em Liderança Feminina")
    input("\nPressione ENTER para sair")

def apoio_psicopedagogico():
    print("\nAPOIO PSICOPEDAGÓGICO")
    print("Esta é uma simulação de contato.")
    print("Mensagem: 'Estamos aqui para te apoiar! Envie um e-mail para apoio@conectagirl.org'")
    input("\nPressione ENTER para sair")

def editar_perfil(email):
    print("\nEDITAR PERFIL")
    novo_nome = input(f"Novo nome ({usuarios[email]['nome']}): ") or usuarios[email]['nome']
    nova_senha = input("Nova senha (deixe em branco para manter): ") or usuarios[email]['senha']

    usuarios[email]['nome'] = novo_nome
    usuarios[email]['senha'] = nova_senha

    salvar_usuarios()

    print("Dados alterados com sucesso!")

def iniciar_sistema():
    carregar_usuarios()
    print("BEM-VINDA AO CONECTA GIRL")

    while True:
        opcao = menu_principal()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            login()
        elif opcao == "3":
            ver_noticias()
        else:
            print("Opção inválida!")

iniciar_sistema()
