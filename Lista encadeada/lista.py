class No:
    def __init__(self, valor):
        self.valor = valor
        self.proximo = None

class ListaEncadeada:
    def __init__(self):
        self.inicio = None
        self._tamanho = 0

    def esta_vazia(self):
        return self.inicio is None

    def tamanho(self):
        return self._tamanho

    def obter_elemento(self, posicao):
        if posicao < 1 or posicao > self._tamanho:
            raise IndexError("Posicao invalida.")
        atual = self.inicio
        for _ in range(1, posicao):
            atual = atual.proximo
        return atual.valor

    def modificar_elemento(self, posicao, valor):
        if posicao < 1 or posicao > self._tamanho:
            raise IndexError("Posicao invalida.")
        atual = self.inicio
        for _ in range(1, posicao):
            atual = atual.proximo
        atual.valor = valor

    def inserir_elemento(self, posicao, valor):
        if posicao < 1 or posicao > self._tamanho + 1:
            raise IndexError("Posicao invalida.")
        novo = No(valor)
        if posicao == 1:
            novo.proximo = self.inicio
            self.inicio = novo
        else:
            anterior = self.inicio
            for _ in range(1, posicao - 1):
                anterior = anterior.proximo
            novo.proximo = anterior.proximo
            anterior.proximo = novo
        self._tamanho += 1

    def remover_elemento(self, posicao):
        if posicao < 1 or posicao > self._tamanho:
            raise IndexError("Posicao invalida.")
        if posicao == 1:
            removido = self.inicio
            self.inicio = removido.proximo
        else:
            anterior = self.inicio
            for _ in range(1, posicao - 1):
                anterior = anterior.proximo
            removido = anterior.proximo
            anterior.proximo = removido.proximo
        self._tamanho -= 1
        return removido.valor

    def imprimir_lista(self):
        atual = self.inicio
        elementos = []
        while atual:
            elementos.append(str(atual.valor))
            atual = atual.proximo
        return " -> ".join(elementos) if elementos else "Lista vazia"
