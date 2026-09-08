
import os
from pathlib import Path
from colorama import init, Fore, Style

# Faz as cores resetarem sozinhas depois de cada print, sem precisar
# ficar escrevendo Style.RESET_ALL toda hora.
init(autoreset=True)


def pausar():
    """Só espera o usuário apertar ENTER antes de voltar pro menu."""
    input("\nENTER para voltar...")


def ls():
    """
    Simula o comando 'ls': lista o que tem na pasta atual.
    Também mostra se o usuário quer ver os arquivos ocultos (que começam com '.'),
    igual o 'ls -a' de verdade.
    """
    print("\nQuer ver os arquivos ocultos também? (aqueles que começam com '.')")
    resposta = input("Mostrar ocultos? (s/n): ").strip().lower()
    mostrar_ocultos = resposta == "s"

    itens = os.listdir()

    # Se o usuário não quiser ver ocultos, a gente filtra a lista antes de mostrar.
    if not mostrar_ocultos:
        itens = [item for item in itens if not item.startswith(".")]

    itens.sort()

    print("\nConteúdo da pasta:\n")

    if not itens:
        print(Fore.YELLOW + "Essa pasta está vazia.")
    else:
        for item in itens:
            if os.path.isdir(item):
                print(Fore.BLUE + "[PASTA]   " + item)
            else:
                print("[ARQUIVO] " + item)

    pausar()


def cat():
    """
    Simula o comando 'cat': mostra o conteúdo de um ou mais arquivos.
    Dá pra digitar mais de um nome de arquivo separado por espaço,
    igual o cat de verdade faz (cat arquivo1.txt arquivo2.txt).
    """
    entrada = input("\nNome do(s) arquivo(s), separados por espaço: ")
    nomes_dos_arquivos = entrada.split()

    if not nomes_dos_arquivos:
        print(Fore.YELLOW + "\nVocê não digitou nenhum arquivo.")
        pausar()
        return

    for nome in nomes_dos_arquivos:
        # Se for mais de um arquivo, mostra o nome antes do conteúdo,
        # pra não ficar tudo misturado.
        if len(nomes_dos_arquivos) > 1:
            print(Fore.CYAN + f"\n--- {nome} ---")

        try:
            with open(nome, "r", encoding="utf-8") as arquivo:
                print(arquivo.read())
        except FileNotFoundError:
            print(Fore.RED + f"Não encontrei o arquivo '{nome}'.")
        except IsADirectoryError:
            print(Fore.RED + f"'{nome}' é uma pasta, não um arquivo.")
        except PermissionError:
            print(Fore.RED + f"Sem permissão para abrir '{nome}'.")
        except UnicodeDecodeError:
            print(Fore.RED + f"'{nome}' parece ser um arquivo binário, não dá pra mostrar como texto.")

    pausar()


def echo():
    """
    Simula o comando 'echo': só repete de volta o que a pessoa digitou.
    """
    texto = input("\nDigite o texto: ")
    print("\n" + texto)
    pausar()


def tee():
    """
    Simula o comando 'tee': salva um texto dentro de um arquivo.
    Pergunta se é pra substituir o conteúdo antigo ou só adicionar no final.
    """
    nome = input("\nNome do arquivo: ").strip()

    if not nome:
        print(Fore.YELLOW + "\nVocê precisa digitar um nome de arquivo.")
        pausar()
        return

    texto = input("Texto que vai ser salvo: ")

    print("\nO que você quer fazer com esse arquivo?")
    print("1 - Substituir tudo que já tinha nele")
    print("2 - Adicionar esse texto no final, sem apagar o resto")
    modo = input("Escolha (1 ou 2): ")

    if modo not in ("1", "2"):
        print(Fore.YELLOW + "\nOpção inválida, tente de novo.")
        pausar()
        return

    modo_de_abertura = "w" if modo == "1" else "a"

    try:
        with open(nome, modo_de_abertura, encoding="utf-8") as arquivo:
            arquivo.write(texto + "\n")
        # O 'tee' de verdade não só salva no arquivo, ele também mostra
        # o texto na tela ao mesmo tempo. Por isso o print aqui também.
        print("\n" + texto)
        print(Fore.GREEN + "\nProntinho, arquivo salvo!")
    except IsADirectoryError:
        print(Fore.RED + f"\n'{nome}' é uma pasta, não dá pra escrever nela.")
    except PermissionError:
        print(Fore.RED + f"\nSem permissão para escrever em '{nome}'.")

    pausar()


def limpar_tela():
    """Limpa a tela do terminal (funciona no Windows e no Linux/Mac)."""
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_titulo():
    print(Fore.MAGENTA + Style.BRIGHT + "=== TERMINAL PYTHON ===")


def menu():
    """Menu principal: fica repetindo até o usuário escolher sair."""
    while True:
        limpar_tela()
        mostrar_titulo()

        print("\nEscolha um comando:")
        print("1 - ls    (listar arquivos da pasta)")
        print("2 - cat   (mostrar conteúdo de um arquivo)")
        print("3 - echo  (repetir um texto)")
        print("4 - tee   (salvar um texto em um arquivo)")
        print("0 - sair")

        escolha = input(Fore.CYAN + "\nuser@python:~$ ")

        if escolha == "1":
            ls()
        elif escolha == "2":
            cat()
        elif escolha == "3":
            echo()
        elif escolha == "4":
            tee()
        elif escolha == "0":
            limpar_tela()
            print(Fore.GREEN + "Até mais! Programa encerrado.")
            break
        else:
            print(Fore.YELLOW + "\nOpção inválida, escolha um número do menu.")
            pausar()


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        # Se o usuário apertar Ctrl+C, sai de forma tranquila em vez de
        # mostrar um erro feio na tela.
        print(Fore.GREEN + "\n\nAté mais! Programa encerrado.")