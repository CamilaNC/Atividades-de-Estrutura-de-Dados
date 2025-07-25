from lista import ListaSequencial
import os

class MenuListaSequencial:
    def __init__(self):
        self.lista = None
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_cabecalho(self):
        print("=======================================")
        print("| LISTA SEQUENCIAL - MENU INTERATIVO |")
        print("=======================================")
        
        if self.lista:
            print(f"\nCapacidade: {self.lista.capacidade} | Tamanho atual: {self.lista.tamanho}")
            print(f"Lista: {self.lista}")
    
    def aguardar_enter(self):
        input("\nPressione Enter para continuar...")
    
    def configurar_lista(self):
        self.limpar_tela()
        print("================================")
        print("| CONFIGURACAO INICIAL DA LISTA |")
        print("================================")
        
        while True:
            try:
                capacidade = int(input("\nDigite a capacidade máxima da lista: "))
                if capacidade <= 0:
                    raise ValueError("A capacidade deve ser um número positivo")
                self.lista = ListaSequencial(capacidade)
                break
            except ValueError as e:
                print(f"Erro: {e}")
    
    def menu_principal(self):
        while True:
            self.limpar_tela()
            self.exibir_cabecalho()
            
            print("\nOPÇÕES DISPONÍVEIS:")
            print("1. Inserir elemento")
            print("2. Modificar elemento")
            print("3. Remover elemento")
            print("4. Consultar elemento")
            print("5. Visualizar lista completa")
            print("6. Informações da lista")
            print("7. Verificar status")
            print("0. Sair do programa")
            
            try:
                opcao = input("\nEscolha uma opção: ")
                
                if opcao == "1":
                    self.inserir_elemento()
                elif opcao == "2":
                    self.modificar_elemento()
                elif opcao == "3":
                    self.remover_elemento()
                elif opcao == "4":
                    self.consultar_elemento()
                elif opcao == "5":
                    self.visualizar_lista()
                elif opcao == "6":
                    self.informacoes_lista()
                elif opcao == "7":
                    self.verificar_status()
                elif opcao == "0":
                    print("\nEncerrando o programa...")
                    break
                else:
                    print("Opção inválida! Tente novamente.")
                    self.aguardar_enter()
            
            except Exception as e:
                print(f"\nErro: {e}")
                self.aguardar_enter()
    
    def inserir_elemento(self):
        self.limpar_tela()
        print("=========================")
        print("| INSERIR NOVO ELEMENTO |")
        print("=========================")
        
        print(f"\nPosições válidas: 1 a {self.lista.tamanho + 1}")
        pos = int(input("Posição para inserir: "))
        val = int(input("Valor a ser inserido: "))
        
        self.lista.inserir_elemento(pos, val)
        print(f"\nElemento {val} inserido na posição {pos} com sucesso!")
        self.aguardar_enter()
    
    def modificar_elemento(self):
        self.limpar_tela()
        print("==============================")
        print("| MODIFICAR ELEMENTO EXISTENTE |")
        print("==============================")
        
        print(f"\nPosições válidas: 1 a {self.lista.tamanho}")
        pos = int(input("Posição do elemento a modificar: "))
        val = int(input("Novo valor: "))
        
        self.lista.modificar_elemento(pos, val)
        print(f"\nPosição {pos} modificada para o valor {val}!")
        self.aguardar_enter()
    
    def remover_elemento(self):
        self.limpar_tela()
        print("=======================")
        print("| REMOVER ELEMENTO |")
        print("=======================")
        
        print(f"\nPosições válidas: 1 a {self.lista.tamanho}")
        pos = int(input("Posição do elemento a remover: "))
        
        removido = self.lista.remover_elemento(pos)
        print(f"\nElemento {removido} removido da posição {pos}!")
        self.aguardar_enter()
    
    def consultar_elemento(self):
        self.limpar_tela()
        print("========================")
        print("| CONSULTAR ELEMENTO |")
        print("========================")
        
        print(f"\nPosições válidas: 1 a {self.lista.tamanho}")
        pos = int(input("Posição do elemento a consultar: "))
        
        elemento = self.lista.obter_elemento(pos)
        print(f"\nElemento na posição {pos}: {elemento}")
        self.aguardar_enter()
    
    def visualizar_lista(self):
        self.limpar_tela()
        print("===============================")
        print("| VISUALIZACAO COMPLETA DA LISTA |")
        print("===============================")
        
        print("\nESTRUTURA COMPLETA:")
        for i in range(self.lista.capacidade):
            marcador = ">" if i < self.lista.tamanho else " "
            valor = self.lista.dados[i] if i < self.lista.tamanho else "VAZIO"
            print(f"[{i+1:02d}]{marcador} {valor}")
        
        self.aguardar_enter()
    
    def informacoes_lista(self):
        self.limpar_tela()
        print("========================")
        print("| INFORMACOES DA LISTA |")
        print("========================")
        
        print(f"\nCapacidade máxima: {self.lista.capacidade}")
        print(f"Elementos armazenados: {self.lista.tamanho}")
        print(f"Espaços disponíveis: {self.lista.capacidade - self.lista.tamanho}")
        print(f"Lista está vazia? {'SIM' if self.lista.esta_vazia() else 'NÃO'}")
        print(f"Lista está cheia? {'SIM' if self.lista.esta_cheia() else 'NÃO'}")
        
        self.aguardar_enter()
    
    def verificar_status(self):
        self.limpar_tela()
        print("=======================")
        print("| STATUS DE OPERACAO |")
        print("=======================")
        
        if self.lista.esta_vazia():
            print("\nATENÇÃO: A lista está VAZIA!")
        elif self.lista.esta_cheia():
            print("\nATENÇÃO: A lista está CHEIA!")
        else:
            print("\nStatus: Operação normal")
        
        print(f"\nElementos: {self.lista.tamanho}/{self.lista.capacidade}")
        self.aguardar_enter()

def main():
    sistema = MenuListaSequencial()
    sistema.configurar_lista()
    sistema.menu_principal()

if __name__ == "__main__":
    main()