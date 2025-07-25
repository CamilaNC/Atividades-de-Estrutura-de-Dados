import unittest
from lista import ListaSequencial
import os
import sys

result_path = os.path.join(os.path.dirname(__file__), "resultados_testes.txt")
sys.stdout = open(result_path, "w", encoding="utf-8")

class TestListaSequencial(unittest.TestCase):

    def test_inserir_e_obter(self):
        print("=== Teste: Inserir e Obter ===")
        lista = ListaSequencial(10)
        lista.inserir_elemento(1, 42)
        print("Lista após inserção:", lista.obter_lista())
        self.assertEqual(lista.obter_elemento(1), 42)
        print()

    def test_modificar(self):
        print("=== Teste: Modificar ===")
        lista = ListaSequencial(3)
        lista.inserir_elemento(1, 10)
        lista.modificar_elemento(1, 99)
        print("Lista após modificação:", lista.obter_lista())
        self.assertEqual(lista.obter_elemento(1), 99)
        print()

    def test_remover(self):
        print("=== Teste: Remover ===")
        lista = ListaSequencial(3)
        lista.inserir_elemento(1, 5)
        lista.inserir_elemento(2, 15)
        removido = lista.remover_elemento(1)
        print(f"Elemento removido: {removido}")
        print("Lista após remoção:", lista.obter_lista())
        self.assertEqual(removido, 5)
        self.assertEqual(lista.obter_elemento(1), 15)
        print()

    def test_limites_invalidos(self):
        print("=== Teste: Limites Inválidos ===")
        lista = ListaSequencial(5)
        try:
            lista.obter_elemento(0)
        except IndexError:
            print("Erro ao obter posição 0 detectado com sucesso.")

        try:
            lista.inserir_elemento(0, 10)
        except IndexError:
            print("Erro ao inserir na posição 0 detectado com sucesso.")

        try:
            lista.remover_elemento(1)
        except ValueError:
            print("Erro ao remover de lista vazia detectado com sucesso.")
        print()

    def test_lista_cheia(self):
        print("=== Teste: Lista Cheia ===")
        lista = ListaSequencial(1)
        lista.inserir_elemento(1, 1)
        print("Lista após inserção:", lista.obter_lista())
        try:
            lista.inserir_elemento(2, 2)
        except OverflowError:
            print("Erro ao inserir em lista cheia detectado com sucesso.")
        print()

if __name__ == '__main__':
    unittest.main()
