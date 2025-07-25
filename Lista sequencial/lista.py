class ListaSequencial:
    def __init__(self, capacidade=100):
        self.dados = [None] * capacidade  # Usando None em vez de 0
        self.tamanho = 0
        self.capacidade = capacidade

    def __str__(self):
        return str([self.dados[i] for i in range(self.tamanho)])

    def _validar_posicao(self, posicao, incluir_fim=False):
        limite = self.tamanho + 1 if incluir_fim else self.tamanho
        if not 1 <= posicao <= limite:
            raise IndexError(f"Posição inválida: {posicao}. Deve estar entre 1 e {limite}")

    def esta_vazia(self):
        return self.tamanho == 0

    def esta_cheia(self):
        return self.tamanho == self.capacidade

    def obter_tamanho(self):
        return self.tamanho

    def obter_elemento(self, posicao):
        self._validar_posicao(posicao)
        return self.dados[posicao - 1]

    def modificar_elemento(self, posicao, novo_valor):
        self._validar_posicao(posicao)
        self.dados[posicao - 1] = novo_valor

    def inserir_elemento(self, posicao, valor):
        if self.esta_cheia():
            raise OverflowError("Lista cheia - capacidade máxima atingida")
        self._validar_posicao(posicao, incluir_fim=True)
        
        # Deslocar elementos para abrir espaço
        for i in range(self.tamanho, posicao - 1, -1):
            self.dados[i] = self.dados[i - 1]
        
        self.dados[posicao - 1] = valor
        self.tamanho += 1

    def remover_elemento(self, posicao):
        if self.esta_vazia():
            raise ValueError("Lista vazia - não há elementos para remover")
        self._validar_posicao(posicao)
        
        valor_removido = self.dados[posicao - 1]
        
        # Deslocar elementos para preencher o espaço
        for i in range(posicao, self.tamanho):
            self.dados[i - 1] = self.dados[i]
        
        self.tamanho -= 1
        return valor_removido
    
    def obter_lista(self):
        return self.dados[:self.tamanho]
