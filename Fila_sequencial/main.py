from fila import Fila

def menu():
    print("\n==== MENU FILA CIRCULAR DINÂMICA ====")
    print("1 - Inserir valor")
    print("2 - Remover valor")
    print("3 - Consultar início da fila")
    print("4 - Verificar se fila está vazia")
    print("5 - Verificar se fila está cheia")
    print("0 - Sair")

def main():
    while True:
        try:
            tamanho = int(input("Digite o tamanho máximo da fila: "))
            if tamanho <= 0:
                raise ValueError
            break
        except ValueError:
            print("Tamanho inválido. Digite um número inteiro positivo.")

    fila = Fila(tamanho)

    while True:
        menu()
        try:
            opcao = int(input("Escolha uma opção: "))
        except ValueError:
            print("Opção inválida! Digite um número.")
            continue

        if opcao == 1:
            try:
                valor = int(input("Digite um valor inteiro para inserir: "))
                if fila.inserir(valor):
                    print(f"Valor {valor} inserido com sucesso!")
                else:
                    print("Fila cheia! Não é possível inserir.")
            except ValueError:
                print("Valor inválido. Digite um número inteiro.")
        elif opcao == 2:
            removido = fila.remover()
            if removido is None:
                print("Fila vazia! Nada a remover.")
            else:
                print(f"Valor removido: {removido}")
        elif opcao == 3:
            inicio = fila.consultar_inicio()
            if inicio is None:
                print("Fila vazia!")
            else:
                print(f"Início da fila: {inicio}")
        elif opcao == 4:
            print("Fila está vazia!" if fila.esta_vazia() else "Fila NÃO está vazia.")
        elif opcao == 5:
            print("Fila está cheia!" if fila.esta_cheia() else "Fila NÃO está cheia.")
        elif opcao == 0:
            print("Encerrando programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
