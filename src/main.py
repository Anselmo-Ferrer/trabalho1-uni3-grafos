"""
UVA 1235 - Anti Brute Force Lock

Modelagem como grafo:
    - Cada chave de 4 digitos vira um vertice.
    - O peso da aresta entre duas chaves a e b e a soma, para
      cada uma das 4 posicoes, de min(|a_i - b_i|, 10 - |a_i - b_i|).
      Esta e a quantidade minima de giros para transformar a em b,
      considerando o caractere de roda circular (apos 9 vem 0).

Por que MST resolve:
    - O cadeado comeca em 0000. Apos desbloquear uma chave, o
      botao JUMP permite teletransportar de graca para qualquer
      chave ja desbloqueada (porem nao para 0000, que nao e uma
      chave desbloqueada).
    - Logo, depois do primeiro giro a partir de 0000, cada nova
      chave pode ser alcancada a partir da chave desbloqueada
      mais barata. Isso constroi exatamente uma arvore geradora
      minima entre as chaves.
    - Resta somar a primeira saida de 0000. Como apos a primeira
      saida nao se pode mais retornar de graca a 0000, basta
      escolher a chave inicial mais proxima de 0000.

Formula:
    resposta = MST(chaves) + min_{k em chaves} dist(0000, k)

Algoritmo: Kruskal com Union-Find por tamanho e compressao de
caminho. Complexidade O(N^2 log N) por caso (N ate 500).
"""

import sys

from edge import Edge
from kruskal_mst import KruskalMST


DIGIT_DIST = [[min(abs(a - b), 10 - abs(a - b)) for b in range(10)]
              for a in range(10)]


def key_distance(a, b):
    return (DIGIT_DIST[a[0]][b[0]] + DIGIT_DIST[a[1]][b[1]]
            + DIGIT_DIST[a[2]][b[2]] + DIGIT_DIST[a[3]][b[3]])


def parse_key(token):
    token = token.zfill(4)
    return (int(token[0]), int(token[1]), int(token[2]), int(token[3]))


ZERO = (0, 0, 0, 0)


def solve(keys):
    n = len(keys)
    # Custo da primeira saida de 0000: a chave mais proxima.
    min_from_zero = min(key_distance(ZERO, k) for k in keys)

    if n == 1:
        return min_from_zero

    # Grafo completo entre as chaves: uma aresta para cada par.
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            edges.append(Edge(i, j, key_distance(keys[i], keys[j])))

    mst = KruskalMST(n, edges)
    return mst.weight + min_from_zero


def main():
    data = sys.stdin.read().split()
    idx = 0
    t = int(data[idx]); idx += 1
    out = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        keys = []
        for _ in range(n):
            keys.append(parse_key(data[idx])); idx += 1
        out.append(str(solve(keys)))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
