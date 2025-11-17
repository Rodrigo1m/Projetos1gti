
# Sistema: CONECTA GIRL
# Linguagem: Python
# Persistencia: grava/recupera usuarios em usuarios.json
# Explicacao para vcs: arquivo com CRUD basico para usuarias.
# - Mantemos os dados em memoria em `usuarios`.
# - Salvamos/recuperamos de `usuarios.json` para persistencia entre sessoes.
# - Funcoes separadas por responsabilidades: utilitarios, persistencia,
#   operacoes CRUD e interface (menu).

import json
import os
import re
import sys

# Simulacao de "banco de dados" de usuarias (em memoria)
usuarios = {}

# Arquivo onde os dados serao persistidos
DATA_FILE = "usuarios.json"


# Utilitarios de entrada
# Explicacao para vcs:
# Use safe_input para ler do usuario. Ela trata Ctrl+C/Ctrl+D e evita crash.
def safe_input(prompt: str, required: bool = False) -> str | None:
    """
    Entrada segura que captura EOFError / KeyboardInterrupt.
    - Se o usuario cancelar (Ctrl+D/Ctrl+C), retorna None para o chamador tratar.
    - Se required=True, repete ate que o usuario informe um valor nao vazio
      ou cancele a operacao.
    """
    try:
        while True:
            value = input(prompt)
            if value is None:
                return None
            value = value.strip()
            if required and value == "":
                print("Campo obrigatorio. Por favor, informe um valor valido.")
                continue
            return value
    except (EOFError, KeyboardInterrupt):
        print("\nEntrada cancelada pelo usuario. Retornando ao menu...")
        return None


# Validacao basica de formato de email.
def validar_email(email: str) -> bool:
    """Validacao basica de formato de e-mail."""
    if not email:
        return False
    pattern = r"^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+$"
    return re.match(pattern, email) is not None


# Persistencia em arquivo
# Explicacao para vcs:
# salvar_usuarios escreve o dicionario em JSON; carregar_usuarios recupera.
# Tratamos excecoes para evitar que dados corrompidos quebrem o app.
def salvar_usuarios():
    """Salva o dicionario `usuarios` no arquivo DATA_FILE em formato JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Erro ao salvar usuarios: {e}")


def carregar_usuarios():
    """Carrega os usuarios do arquivo DATA_FILE para o dicionario `usuarios` (global)."""
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
                print("Formato de arquivo invalido. Esperado um objeto JSON. Iniciando vazio.")
                usuarios = {}
    except json.JSONDecodeError:
        print("Arquivo de dados corrompido (JSON invalido). Iniciando com base vazia.")
        usuarios = {}
    except Exception as e:
        print(f"Erro ao carregar usuarios: {e}")
        usuarios = {}


# Operacoes CRUD

# Explicacao para vcs:
# Create: cadastrar_usuario
# Read: listar_usuarios_salvos, ver_usuario_por_email
# Update: editar_perfil
# Delete: deletar_conta
def cadastrar_usuario():
    # Create: pede nome, email e senha com validacoes basicas.
    print("\n--- CADASTRO DE USUARIA ---")
    nome = safe_input("Nome: ", required=True)
    if nome is None:
        return
    email = safe_input("E-mail: ", required=True)
    if email is None:
        return
    if not validar_email(email):
        print("E-mail invalido. Operacao cancelada.")
        return
    senha = safe_input("Senha: ", required=True)
    if senha is None:
        return

    if email in usuarios:
        print("E-mail ja cadastrado!")
        return

    usuarios[email] = {"nome": nome, "senha": senha}
    salvar_usuarios()
    print("Usuaria criada com sucesso e salva em arquivo.")
    safe_input("Pressione ENTER para continuar...")


def ver_usuario_por_email():
    # Read (detalhada): mostra dados basicos de uma usuaria pelo email
    print("\n--- VER USUARIA POR E-MAIL ---")
    email = safe_input("E-mail da usuaria: ", required=True)
    if email is None:
        return
    if email not in usuarios:
        print("Usuaria nao encontrada.")
    else:
        info = usuarios[email]
        print("\nDados da usuaria:")
        print(f"Nome : {info.get('nome', '<sem nome>')}")
        print(f"E-mail: {email}")
        print("Senha: <oculta>")
    safe_input("Pressione ENTER para retornar...")


def listar_usuarios_salvos():
    # Read (lista): exibe todas as usuarias salvas em memoria
    print("\n--- USUARIAS SALVAS (arquivo) ---")
    if not usuarios:
        print("Nenhuma usuaria salva.")
    else:
        for email, info in usuarios.items():
            nome = info.get("nome", "<sem nome>")
            print(f" - {nome} <{email}> | senha: <oculta>")
    safe_input("Pressione ENTER para retornar...")


def editar_perfil(email_logado: str):
    # Update: altera nome e senha da usuaria logada
    if email_logado not in usuarios:
        print("Usuaria nao encontrada.")
        return
    print("\n--- EDITAR PERFIL ---")
    atual = usuarios[email_logado]
    novo_nome = safe_input(f"Novo nome ({atual['nome']}) [ENTER para manter]: ")
    if novo_nome is None:
        return
    if novo_nome == "":
        novo_nome = atual['nome']

    nova_senha = safe_input("Nova senha (deixe em branco para manter): ")
    if nova_senha is None:
        return
    if nova_senha == "":
        nova_senha = atual['senha']

    if novo_nome.strip() == "" or nova_senha.strip() == "":
        print("Nome e senha nao podem ficar vazios. Operacao cancelada.")
        return

    usuarios[email_logado]['nome'] = novo_nome
    usuarios[email_logado]['senha'] = nova_senha
    salvar_usuarios()
    print("Dados alterados com sucesso e salvos em arquivo.")
    safe_input("Pressione ENTER para continuar...")


def deletar_conta(email_logado: str):
    # Delete: remove a conta da usuaria apos confirmacao
    if email_logado not in usuarios:
        print("Usuaria nao encontrada.")
        return
    print("\n--- DELETAR CONTA ---")
    confirm = safe_input("Tem certeza que deseja excluir sua conta? Digite 'SIM' para confirmar: ")
    if confirm is None or confirm.upper() != "SIM":
        print("Operacao cancelada.")
        return
    try:
        usuarios.pop(email_logado, None)
        salvar_usuarios()
        print("Conta removida com sucesso.")
    except Exception as e:
        print(f"Erro ao remover conta: {e}")
    safe_input("Pressione ENTER para retornar ao menu principal.")


# -------------------------
# Partes do UI / Menu
# -------------------------
# Explicacao para vcs:
# Menu principal simples; se precisarmos expandir, manter o dispatcher limpo.
def menu_principal():
    print("\n==== MENU PRINCIPAL ====")
    print("1 - Cadastrar usuaria")
    print("2 - Login")
    print("3 - Ver Noticias")
    print("4 - Listar usuarias salvas (arquivo)")
    print("5 - Ver usuaria por e-mail")
    print("0 - Sair")
    opcao = safe_input("Escolha uma opcao: ", required=True)
    return opcao


def login():
    # Fluxo de login: verifica email e senha no dicionario usuarios
    print("\n--- LOGIN ---")
    email = safe_input("E-mail: ", required=True)
    if email is None:
        return
    senha = safe_input("Senha: ", required=True)
    if senha is None:
        return

    if email in usuarios and usuarios[email]["senha"] == senha:
        print("Login bem-sucedido!")
        painel_usuaria(email)
    else:
        print("E-mail ou senha incorretos.")


def ver_noticias():
    # Mensagens estaticas para demonstracao
    print("\n--- NOTICIAS ---")
    print("1. Projeto Conecta Girl promove mentoria para jovens mulheres.")
    print("2. Novas bolsas de estudo disponiveis para tecnologia.")
    print("3. Evento online: Mulheres na Ciencia e Inovacao.")
    safe_input("\nPressione ENTER para retornar ao menu principal.")


def painel_usuaria(email):
    # Painel apos login; delega operacoes para funcoes especificas
    while True:
        usu = usuarios.get(email)
        if usu is None:
            print("Usuaria nao encontrada. Retornando ao menu principal.")
            return
        print(f"\n=== PAINEL DA USUARIA ({usu['nome']}) ===")
        print("1 - Ver oportunidades")
        print("2 - Apoio psicopedagogico")
        print("3 - Editar perfil")
        print("4 - Deletar conta")
        print("5 - Logout")
        opcao = safe_input("Escolha uma opcao: ", required=True)
        if opcao is None:
            continue

        if opcao == "1":
            ver_oportunidades()
        elif opcao == "2":
            apoio_psicopedagogico()
        elif opcao == "3":
            editar_perfil(email)
        elif opcao == "4":
            deletar_conta(email)
            return
        elif opcao == "5":
            print("Sessao encerrada. Retornando ao menu principal...")
            return
        else:
            print("Opcao invalida. Tente novamente.")


def ver_oportunidades():
    # Conteudo estatico de exemplo
    print("\n--- OPORTUNIDADES ---")
    print("1. Estagio em Tecnologia - Empresa Tech4Girls")
    print("2. Bolsa de estudos em Programacao - Instituto Mulheres Digitais")
    print("3. Mentoria gratuita em Lideranca Feminina")
    safe_input("\nPressione ENTER para sair...")


def apoio_psicopedagogico():
    # Simulacao de contato; em produto real, chamar um servico
    print("\n--- APOIO PSICOPEDAGOGICO ---")
    print("Esta e uma simulacao de contato.")
    print("Mensagem: 'Estamos aqui para te apoiar! Envie um e-mail para apoio@conectagirl.org'")
    safe_input("\nPressione ENTER para sair...")


# Inicio do sistema
# Explicacao para vcs: carregamos usuarios ao iniciar e entramos no loop principal.
def iniciar_sistema():
    print("=== BEM-VINDA AO CONECTA GIRL ===")
    carregar_usuarios()
    try:
        while True:
            opcao = menu_principal()
            if opcao is None:
                continue

            if opcao == "1":
                cadastrar_usuario()
            elif opcao == "2":
                login()
            elif opcao == "3":
                ver_noticias()
            elif opcao == "4":
                listar_usuarios_salvos()
            elif opcao == "5":
                ver_usuario_por_email()
            elif opcao == "0":
                print("Saindo do sistema. Ate logo!")
                break
            else:
                print("Opcao invalida. Tente novamente.")
    except Exception as e:
        # Erro inesperado: tentamos salvar o estado antes de sair
        print(f"Erro inesperado: {e}")
        try:
            salvar_usuarios()
        except Exception:
            pass
        print("Encerrando programa devido a erro.")
        sys.exit(1)


# Executar sistema
if __name__ == "__main__":
    iniciar_sistema()
