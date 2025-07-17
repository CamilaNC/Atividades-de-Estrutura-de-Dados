import os
import time
import shutil
from typing import List, Tuple
from ordenacao import selection_sort, insertion_sort

def limpar_pasta_resultados():
    pasta = "resultados"
    if os.path.exists(pasta):
        shutil.rmtree(pasta)
    os.makedirs(pasta)

def carregar_arquivo(caminho: str) -> List[int]:
    try:
        with open(caminho, 'r') as f:
            return [int(linha.strip()) for linha in f if linha.strip()]
    except Exception as e:
        print(f"Erro ao ler {caminho}: {str(e)}")
        return []

def verificar_ordenacao(arr: List[int]) -> bool:
    return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

def salvar_resultado(lista: List[int], nome_arquivo: str, algoritmo: str):
    caminho = os.path.join("resultados", f"{algoritmo}_{nome_arquivo}")
    with open(caminho, 'w') as f:
        f.write('\n'.join(map(str, lista)))

def escrever_relatorio(nome_arquivo: str, tamanho: int, tempo_sel: float, tempo_ins: float):
    relatorio_path = os.path.join("resultados", "relatorio.txt")
    cabecalho = ("="*60 + "\n" + "RELATÓRIO DE ORDENAÇÃO".center(60) + "\n" + "="*60 + "\n") 
    if not os.path.exists(relatorio_path):
        with open(relatorio_path, 'w') as rel:
            rel.write(cabecalho)
    
    with open(relatorio_path, 'a') as rel:
        rel.write(f"\nArquivo: {nome_arquivo}\n")
        rel.write(f"Tamanho: {tamanho:,}\n")
        rel.write(f"Selection Sort: {tempo_sel:.6f}s\n")
        rel.write(f"Insertion Sort: {tempo_ins:.6f}s\n")
        rel.write("-"*60 + "\n")

def executar_testes():
    limpar_pasta_resultados()
    pasta_entrada = "instancias-num"
    arquivos = sorted([f for f in os.listdir(pasta_entrada) if f.endswith(".in")])
    if not arquivos:
        print(f"Nenhum arquivo .in encontrado na pasta '{pasta_entrada}'")
        return

    while True:
        print("\nArquivos disponiveis:")
        for i, nome in enumerate(arquivos):
            print(f"{i+1}. {nome}")

        try:
            escolha = int(input("\nDigite o numero do arquivo que deseja testar (ou 0 para sair): ")) - 1
            if escolha == -1:
                print("Encerrando o programa...")
                break
            if escolha < 0 or escolha >= len(arquivos):
                print("Escolha inválida.")
                continue
        except ValueError:
            print("Entrada invalida.")
            continue

        nome_arquivo = arquivos[escolha]
        caminho = os.path.join(pasta_entrada, nome_arquivo)
        dados = carregar_arquivo(caminho)
        if not dados:
            print("Arquivo vazio ou invalido.")
            continue

        print("\n" + "="*60)
        print("TESTE DE ALGORITMOS DE ORDENAÇAO".center(60))
        print("="*60)

        print(f"\nArquivo: {nome_arquivo}")
        print(f"Elementos: {len(dados):,}")

        sel_ordenado, tempo_sel = selection_sort(dados)
        correto_sel = verificar_ordenacao(sel_ordenado)
        salvar_resultado(sel_ordenado, nome_arquivo, "selection")

        ins_ordenado, tempo_ins = insertion_sort(dados)
        correto_ins = verificar_ordenacao(ins_ordenado)
        salvar_resultado(ins_ordenado, nome_arquivo, "insertion")

        print("\nRESULTADOS:")
        print(f" - Selection Sort: {tempo_sel:.6f} s | {'CORRETO' if correto_sel else 'INCORRETO'}")
        print(f" - Insertion Sort: {tempo_ins:.6f} s | {'CORRETO' if correto_ins else 'INCORRETO'}")

        if tempo_sel < tempo_ins:
            print(f"Mais rapido: Selection Sort ({tempo_ins / tempo_sel:.2f}x mais rapido)")
        elif tempo_ins < tempo_sel:
            print(f"Mais rapido: Insertion Sort ({tempo_sel / tempo_ins:.2f}x mais rapido)")
        else:
            print("Tempos iguais")

        # Escreve os resultados no relatório
        escrever_relatorio(nome_arquivo, len(dados), tempo_sel, tempo_ins)

        continuar = input("\nDeseja ordenar outro arquivo? (s/n): ").strip().lower()
        if continuar != 's':
            print("Encerrando o programa...")
            break

if __name__ == "__main__":
    executar_testes()