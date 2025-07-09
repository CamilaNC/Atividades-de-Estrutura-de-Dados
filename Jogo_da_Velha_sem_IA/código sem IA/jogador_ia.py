# -*- coding: utf-8 -*-
from jogador import Jogador
from tabuleiro import Tabuleiro
import random

class JogadorIA(Jogador):
    def __init__(self, tabuleiro: Tabuleiro, tipo: int):
        super().__init__(tabuleiro, tipo)

    def getJogada(self):
        return escolher_jogada(self.tabuleiro.matriz, self.tipo)

def escolher_jogada(tabuleiro, jogador):
    oponente = Tabuleiro.JOGADOR_X if jogador == Tabuleiro.JOGADOR_0 else Tabuleiro.JOGADOR_0
    linhas = [(i, [(i, j) for j in range(3)]) for i in range(3)]
    colunas = [(j, [(i, j) for i in range(3)]) for j in range(3)]
    diagonais = [
        ('diag1', [(0,0), (1,1), (2,2)]),
        ('diag2', [(0,2), (1,1), (2,0)])
    ]
    todas = linhas + colunas + diagonais

    def verifica_dupla(alvo):
        for _, posicoes in todas:
            valores = [tabuleiro[i][j] for i,j in posicoes]
            if valores.count(alvo) == 2 and valores.count(Tabuleiro.DESCONHECIDO) == 1:
                return posicoes[valores.index(Tabuleiro.DESCONHECIDO)]
        return None

    def cria_duas_duplas():
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == Tabuleiro.DESCONHECIDO:
                    tabuleiro[i][j] = jogador
                    conta = 0
                    for _, posicoes in todas:
                        valores = [tabuleiro[x][y] for x, y in posicoes]
                        if valores.count(jogador) == 2 and valores.count(Tabuleiro.DESCONHECIDO) == 1:
                            conta += 1
                    tabuleiro[i][j] = Tabuleiro.DESCONHECIDO
                    if conta >= 2:
                        return (i, j)
        return None

    jogada = verifica_dupla(jogador)
    if jogada: return jogada
    jogada = verifica_dupla(oponente)
    if jogada: return jogada
    jogada = cria_duas_duplas()
    if jogada: return jogada

    if tabuleiro[1][1] == Tabuleiro.DESCONHECIDO:
        return (1,1)

    cantos = [(0,0), (0,2), (2,0), (2,2)]
    opostos = {(0,0):(2,2), (0,2):(2,0), (2,0):(0,2), (2,2):(0,0)}
    for canto in cantos:
        i,j = canto
        if tabuleiro[i][j] == oponente:
            i2,j2 = opostos[canto]
            if tabuleiro[i2][j2] == Tabuleiro.DESCONHECIDO:
                return (i2,j2)

    random.shuffle(cantos)
    for i,j in cantos:
        if tabuleiro[i][j] == Tabuleiro.DESCONHECIDO:
            return (i,j)

    for i in range(3):
        for j in range(3):
            if tabuleiro[i][j] == Tabuleiro.DESCONHECIDO:
                return (i,j)

    return None
