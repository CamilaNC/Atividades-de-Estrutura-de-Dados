# -*- coding: utf-8 -*-

class Tabuleiro:
    DESCONHECIDO = 0
    JOGADOR_0 = 1
    JOGADOR_X = 4

    def __init__(self):
        self.matriz = [
            [Tabuleiro.DESCONHECIDO] * 3,
            [Tabuleiro.DESCONHECIDO] * 3,
            [Tabuleiro.DESCONHECIDO] * 3
        ]

    def fazer_jogada(self, linha, coluna, jogador):
        
        if self.matriz[linha][coluna] == Tabuleiro.DESCONHECIDO:
            self.matriz[linha][coluna] = jogador
            return True
        return False

    def tem_campeao(self):
       
        # Verifica linhas e colunas
        for i in range(3):
            # Linhas
            if self.matriz[i][0] == self.matriz[i][1] == self.matriz[i][2] != Tabuleiro.DESCONHECIDO:
                return self.matriz[i][0]
            # Colunas
            if self.matriz[0][i] == self.matriz[1][i] == self.matriz[2][i] != Tabuleiro.DESCONHECIDO:
                return self.matriz[0][i]

        # Diagonais
        if self.matriz[0][0] == self.matriz[1][1] == self.matriz[2][2] != Tabuleiro.DESCONHECIDO:
            return self.matriz[0][0]
        if self.matriz[0][2] == self.matriz[1][1] == self.matriz[2][0] != Tabuleiro.DESCONHECIDO:
            return self.matriz[0][2]

        return Tabuleiro.DESCONHECIDO

    def esta_ocupado(self):
        
        for linha in self.matriz:
            for celula in linha:
                if celula == Tabuleiro.DESCONHECIDO:
                    return False
        return True

    def __str__(self):
        
        simbolos = {Tabuleiro.DESCONHECIDO: ".", Tabuleiro.JOGADOR_0: "O", Tabuleiro.JOGADOR_X: "X"}
        linhas = []
        for linha in self.matriz:
            linhas.append(" ".join(simbolos[celula] for celula in linha))
        return "\n".join(linhas)
