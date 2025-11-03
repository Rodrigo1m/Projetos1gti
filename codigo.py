# ==========================================================
# Sistema: CONECTA GIRL
# Linguagem: Python
# Persistência: grava/recupera usuários em usuarios.json
# ==========================================================

import json
import os

# Simulação de "banco de dados" de usuárias (em memória)
usuarios = {}

# Arquivo onde os dados serão persistidos
DATA_FILE = "usuarios.json"

def salvar_usuarios():
    """Salva o dicionário `usuarios` no arquivo DATA_FILE em formato JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar usuários: {e}")

def carregar_usuarios():
    """Carrega os usuários do arquivo DATA_FILE para o dicionário `usuarios` (global)."""
    global usuarios
    if not os.path.exists(DATA_FILE):
        usuarios = {}
        return
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
            if isinstance(dados, dict):
                usuarios = dados
            else:
                print("Formato de arquivo inválido. Esperado um objeto JSON.")
                usuarios = {}
    except json.JSONDecodeError:
        print("Arquivo de dados corrompido (JSON inválido). Iniciando com base vazia.")
        usuarios = {}
    except Exception as e:
        print(f"Erro ao carregar usuários: {e}")
        usuarios = {}

def menu_principal():
    print("\n==== MENU PRINCIPAL ====")
    print("1 - Cadastrar usuária")
    print("2 - Login")
    print("3 - Ver Notícias")
    print("4 - Listar usuárias salvas (arquivo)")
    print("0 - Sair")
    opcao = input("Escolha uma opção: ")
    return opcao

def cadastrar_usuario():
    print("\n--- CADASTRO DE USUÁRIA ---")
    nome = input("Nome: ")
    email = input("E-mail: ")
    senha = input("Senha: ")

    if email in usuarios:
        print(" E-mail já cadastrado!")
    else:
        usuarios[email] = {"nome": nome, "senha": senha}
        salvar_usuarios()
        print(" Usuária criada com sucesso! (salva em arquivo)")

def login():
    print("\n--- LOGIN ---")
    email = input("E-mail: ")
    senha = input("Senha: ")

    if email in usuarios and usuarios[email]["senha"] == senha:
        print(" Login bem-sucedido!")
        painel_usuaria(email)
    else:
        print(" E-mail ou senha incorretos.")

def ver_noticias():
    print("\n--- NOTÍCIAS ---")
    print(" 1. Projeto Conecta Girl promove mentoria para jovens mulheres.")
    print(" 2. Novas bolsas de estudo disponíveis para tecnologia.")
    print(" 3. Evento online: Mulheres na Ciência e Inovação.")
    input("\nPressione ENTER para retornar ao menu principal.")

def painel_usuaria(email):
    while True:
        print(f"\n=== PAINEL DA USUÁRIA ({usuarios[email]['nome']}) ===")
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
            print(" Sessão encerrada. Retornando ao menu principal...")
            break
        else:
            print(" Opção inválida!")

def ver_oportunidades():
    print("\n--- OPORTUNIDADES ---")
    print(" 1. Estágio em Tecnologia - Empresa Tech4Girls")
    print(" 2. Bolsa de estudos em Programação - Instituto Mulheres Digitais")
    print(" 3. Mentoria gratuita em Liderança Feminina")
    input("\nPressione ENTER para sair...")

def apoio_psicopedagogico():
    print("\n--- APOIO PSICOPEDAGÓGICO ---")
    print(" Esta é uma simulação de contato.")
    print("Mensagem: 'Estamos aqui para te apoiar! Envie um e-mail para apoio@conectagirl.org'")
    input("\nPressione ENTER para sair...")

def editar_perfil(email):
    print("\n--- EDITAR PERFIL ---")
    novo_nome = input(f"Novo nome ({usuarios[email]['nome']}): ") or usuarios[email]['nome']
    nova_senha = input("Nova senha (deixe em branco para manter): ") or usuarios[email]['senha']

    usuarios[email]['nome'] = novo_nome
    usuarios[email]['senha'] = nova_senha

    salvar_usuarios()
    print(" Dados alterados com sucesso! (salvos em arquivo)")

def listar_usuarios_salvos():
    """Lê o arquivo de dados e exibe as usuárias salvas.
    Não imprime as senhas em texto claro — mostra '<oculto>' por segurança."""
    if not os.path.exists(DATA_FILE):
        print("\nArquivo de dados não encontrado. Nenhuma usuária salva.")
        input("\nPressione ENTER para retornar ao menu principal.")
        return

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            dados = json.load(f)
    except json.JSONDecodeError:
        print("\nArquivo de dados corrompido (JSON inválido).")
        input("\nPressione ENTER para retornar ao menu principal.")
        return
    except Exception as e:
        print(f"\nErro ao ler arquivo de dados: {e}")
        input("\nPressione ENTER para retornar ao menu principal.")
        return

    print("\n--- USUÁRIAS SALVAS (arquivo) ---")
    if not dados:
        print(" Nenhuma usuária salva.")
    else:
        for email, info in dados.items():
            nome = info.get("nome", "<sem nome>")
            # Não mostrar senha em claro
            print(f" - {nome} <{email}> | senha: <oculto>")
    input("\nPressione ENTER para retornar ao menu principal.")

# ==========================================================
# Início do sistema
# ==========================================================

def iniciar_sistema():
    print("=== BEM-VINDA AO CONECTA GIRL ===")
    carregar_usuarios()

    while True:
        opcao = menu_principal()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            login()
        elif opcao == "3":
            ver_noticias()
        elif opcao == "4":
            listar_usuarios_salvos()
        elif opcao == "0":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print(" Opção inválida!")

# Executar sistema
if __name__ == "__main__":
    iniciar_sistema()
