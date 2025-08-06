class Fila:
    def __init__(self, tamanho_max):
        self.tamanho_max = tamanho_max
        self.dados = [None] * tamanho_max
        self.inicio = 0
        self.fim = 0
        self.tamanho = 0

    def esta_vazia(self):
        return self.tamanho == 0

    def esta_cheia(self):
        return self.tamanho == self.tamanho_max

    def inserir(self, valor: int) -> bool:
        if self.esta_cheia():
            return False
        self.dados[self.fim] = valor
        self.fim = (self.fim + 1) % self.tamanho_max
        self.tamanho += 1
        return True

    def remover(self):
        if self.esta_vazia():
            return None
        valor = self.dados[self.inicio]
        self.inicio = (self.inicio + 1) % self.tamanho_max
        self.tamanho -= 1
        return valor

    def consultar_inicio(self):
        if self.esta_vazia():
            return None
        return self.dados[self.inicio]
