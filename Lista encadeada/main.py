from lista import ListaEncadeada
import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    lista = ListaEncadeada()
    
    while True:
        limpar_tela()
        print("\n=== MENU LISTA ENCADEADA ===")
        print("1. Inserir elemento")
        print("2. Remover elemento")
        print("3. Modificar elemento")
        print("4. Consultar elemento")
        print("5. Ver tamanho da lista")
        print("6. Verificar se está vazia")
        print("7. Imprimir lista")
        print("8. Sair")
        
        opcao = input("\nEscolha uma opcao: ")
        
        try:
            if opcao == '1':
                valor = int(input("Valor a ser inserido: "))
                posicao = int(input("Posicao para inserir: "))
                lista.inserir_elemento(posicao, valor)
                print(f"\nValor {valor} inserido na posicao {posicao}")
                
            elif opcao == '2':
                posicao = int(input("Posicao para remover: "))
                removido = lista.remover_elemento(posicao)
                print(f"\nValor {removido} removido da posicao {posicao}")
                
            elif opcao == '3':
                posicao = int(input("Posicao para modificar: "))
                novo_valor = int(input("Novo valor: "))
                lista.modificar_elemento(posicao, novo_valor)
                print(f"\nPosicao {posicao} modificada para {novo_valor}")
                
            elif opcao == '4':
                posicao = int(input("Posicao para consultar: "))
                valor = lista.obter_elemento(posicao)
                print(f"\nValor na posicao {posicao}: {valor}")
                
            elif opcao == '5':
                print(f"\nTamanho da lista: {lista.tamanho()}")
                
            elif opcao == '6':
                vazia = "SIM" if lista.esta_vazia() else "NAO"
                print(f"\nLista vazia? {vazia}")
                
            elif opcao == '7':
                if lista.esta_vazia():
                    print("\nA lista está vazia.")
                else:
                    print("\nLista atual:")
                    print(lista.imprimir_lista())
 
            elif opcao == '8':
                print("\nSaindo do programa...")
                break
                
            else:
                print("\nOpcao invalida!")
            
            input("\nPressione Enter para continuar...")
            
        except (ValueError, IndexError) as e:
            print(f"\nErro: {e}")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()