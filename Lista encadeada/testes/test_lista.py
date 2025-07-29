import unittest
import sys
import io
from lista import ListaEncadeada

class TestListaEncadeada(unittest.TestCase):
    def setUp(self):
        self.lista = ListaEncadeada()
        self.output_buffer = io.StringIO()
        sys.stdout = self.output_buffer
        self.print_header = lambda msg: print(f"\n{'='*50}\n{msg.center(50)}\n{'='*50}")
        self.print_step = lambda step, data: print(f"• {step.ljust(15)}: {data}")

    def tearDown(self):
        sys.stdout = sys.__stdout__
        print(self.output_buffer.getvalue())

    def test_inserir_e_obter(self):
        """Teste: Inserir e Obter Elementos"""
        val1, val2 = 10, 20
        pos1, pos2 = 1, 2
        
        self.print_header("TESTE: INSERIR E OBTER ELEMENTOS")
        
        # Inserção
        self.lista.inserir_elemento(pos1, val1)
        self.print_step("Inserido", f"Posição {pos1} = {val1}")
        self.lista.inserir_elemento(pos2, val2)
        self.print_step("Inserido", f"Posição {pos2} = {val2}")
        
        # Obtenção
        resultado = self.lista.obter_elemento(pos2)
        self.print_step("Obtido", f"Posição {pos2} = {resultado}")
        self.print_step("Esperado", f"Posição {pos2} = {val2}")
        
        self.assertEqual(resultado, val2)
        print("Teste concluído com sucesso!")

    def test_lista_vazia_e_tamanho(self):
        """Teste: Lista Vazia e Tamanho"""
        self.print_header("TESTE: LISTA VAZIA E TAMANHO")
        
        tamanho = self.lista.tamanho()
        vazia = self.lista.esta_vazia()
        
        self.print_step("Tamanho", f"{tamanho} (esperado: 0)")
        self.print_step("Lista vazia", f"{vazia} (esperado: True)")
        
        self.assertEqual(tamanho, 0)
        self.assertTrue(vazia)
        print("Teste concluído com sucesso!")

    def test_modificar_elemento(self):
        """Teste: Modificar Elemento"""
        original, novo = 5, 99
        pos = 1
        
        self.print_header("TESTE: MODIFICAR ELEMENTO")
        
        self.lista.inserir_elemento(pos, original)
        self.print_step("Original", f"Posição {pos} = {original}")
        
        self.lista.modificar_elemento(pos, novo)
        self.print_step("Modificado", f"Posição {pos} = {novo}")
        
        resultado = self.lista.obter_elemento(pos)
        self.print_step("Resultado", f"Posição {pos} = {resultado}")
        self.print_step("Esperado", f"Posição {pos} = {novo}")
        
        self.assertEqual(resultado, novo)
        print("Teste concluído com sucesso!")

    def test_remover_elemento(self):
        """Teste: Remover Elemento"""
        valores = [10, 20, 30]
        pos_remover = 2
        
        self.print_header("TESTE: REMOVER ELEMENTO")
        
        # Inserção
        for i, val in enumerate(valores, 1):
            self.lista.inserir_elemento(i, val)
        self.print_step("Lista inicial", f"{valores}")
        
        # Remoção
        esperado = valores[pos_remover-1]
        removido = self.lista.remover_elemento(pos_remover)
        self.print_step("Removido", f"Posição {pos_remover} = {removido}")
        self.print_step("Esperado", f"Posição {pos_remover} = {esperado}")
        
        # Verificação
        tamanho_atual = self.lista.tamanho()
        self.print_step("Tamanho atual", f"{tamanho_atual}")
        self.print_step("Tamanho esperado", f"{len(valores)-1}")
        
        self.assertEqual(removido, esperado)
        self.assertEqual(tamanho_atual, len(valores)-1)
        print("Teste concluído com sucesso!")

    def test_limites_invalidos(self):
        """Teste: Limites Inválidos"""
        self.print_header("TESTE: LIMITES INVÁLIDOS")
        
        testes = [
            ("Obter elemento", lambda: self.lista.obter_elemento(1)),
            ("Inserir elemento", lambda: self.lista.inserir_elemento(2, 100)),
            ("Remover elemento", lambda: self.lista.remover_elemento(1))
        ]
        
        for nome, operacao in testes:
            try:
                operacao()
                self.print_step(nome, "Falhou (não levantou exceção)")
            except IndexError:
                self.print_step(nome, "OK (levantou IndexError)")
        
        print("\nVerificação assertiva:")
        with self.assertRaises(IndexError):
            self.lista.obter_elemento(1)
        with self.assertRaises(IndexError):
            self.lista.inserir_elemento(2, 100)
        with self.assertRaises(IndexError):
            self.lista.remover_elemento(1)
        
        print("Todos os casos de limite inválido foram tratados corretamente!")

if __name__ == '__main__':
    unittest.main()