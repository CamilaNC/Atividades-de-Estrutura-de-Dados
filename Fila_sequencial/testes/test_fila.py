import unittest
from fila import Fila
import os

class TestFila(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        os.makedirs("testes/resultados", exist_ok=True)
        cls.arquivo_resultado = open("testes/resultados/resultados_testes.txt", "w", encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.arquivo_resultado.close()

    def escrever(self, mensagem):
        print(mensagem)
        self.arquivo_resultado.write(mensagem + "\n")

    def test_inserir_e_remover(self):
        self.escrever("Testando inserção e remoção:")
        fila = Fila()

        valores = [1, 2, 3]
        for v in valores:
            resultado = fila.inserir(v)
            self.escrever(f"Inserindo {v} -> {'PASSOU' if resultado else 'FALHOU'}")

        for esperado in valores:
            removido = fila.remover()
            self.escrever(f"Removendo -> Esperado: {esperado}, Obtido: {removido} -> {'PASSOU' if removido == esperado else 'FALHOU'}")

        self.assertIsNone(fila.remover())
        self.escrever("Remover com fila vazia -> Esperado: None -> PASSOU")

    def test_consultar_inicio(self):
        self.escrever("\nTestando consulta do início:")
        fila = Fila()

        inicio = fila.consultar_inicio()
        self.escrever(f"Consulta com fila vazia -> Esperado: None, Obtido: {inicio} -> {'PASSOU' if inicio is None else 'FALHOU'}")

        fila.inserir(42)
        inicio = fila.consultar_inicio()
        self.escrever(f"Consulta após inserir 42 -> Esperado: 42, Obtido: {inicio} -> {'PASSOU' if inicio == 42 else 'FALHOU'}")

if __name__ == "__main__":
    unittest.main(verbosity=0)
