"""
UVA 1235 - Anti Brute Force Lock
Versao de submissao: arquivo unico e autocontido (o juiz compila
apenas um arquivo). E a mesma logica dos modulos em src/
(edge.py, uf.py, kruskal_mst.py, main.py), apenas reunida aqui.

Modelagem: cada chave de 4 digitos e um vertice; o peso entre duas
chaves e a soma das menores rotacoes por digito. A resposta e
MST(chaves) + min_k dist(0000, k), pois apos sair de 0000 so se
pode usar JUMP de graca para chaves ja desbloqueadas.

Algoritmo: Kruskal com Union-Find (por tamanho, com compressao de
caminho). Complexidade O(N^2 log N) por caso (N ate 500).
"""

import sys


# --- Aresta (espelha src/edge.py) ---------------------------------
class Edge:
    def __init__(self, v, w, weight):
        self.v = v
        self.w = w
        self.weight = weight

    def either(self):
        return self.v

    def other(self, v):
        if v == self.v:
            return self.w
        if v == self.w:
            return self.v
        raise ValueError("vertice invalido na aresta")

    def __lt__(self, other):
        return self.weight < other.weight


# --- Union-Find / DSU (espelha src/uf.py) -------------------------
class UF:
    def __init__(self, n):
        self.count = n
        self.id = list(range(n))
        self.sz = [1] * n

    def find(self, p):
        while self.id[p] != p:
            self.id[p] = self.id[self.id[p]]
            p = self.id[p]
        return p

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        root_p = self.find(p)
        root_q = self.find(q)
        if root_p == root_q:
            return
        if self.sz[root_p] < self.sz[root_q]:
            self.id[root_p] = root_q
            self.sz[root_q] += self.sz[root_p]
        else:
            self.id[root_q] = root_p
            self.sz[root_p] += self.sz[root_q]
        self.count -= 1


# --- Kruskal (espelha src/kruskal_mst.py) -------------------------
class KruskalMST:
    def __init__(self, n_vertices, edges):
        self.weight = 0
        self.mst = []
        uf = UF(n_vertices)
        for e in sorted(edges):
            if len(self.mst) >= n_vertices - 1:
                break
            v = e.either()
            w = e.other(v)
            if uf.connected(v, w):
                continue
            uf.union(v, w)
            self.mst.append(e)
            self.weight += e.weight


# --- Modelagem e resolucao (espelha src/main.py) ------------------
DIGIT_DIST = [[min(abs(a - b), 10 - abs(a - b)) for b in range(10)]
              for a in range(10)]

ZERO = (0, 0, 0, 0)


def key_distance(a, b):
    return (DIGIT_DIST[a[0]][b[0]] + DIGIT_DIST[a[1]][b[1]]
            + DIGIT_DIST[a[2]][b[2]] + DIGIT_DIST[a[3]][b[3]])


def parse_key(token):
    token = token.zfill(4)
    return (int(token[0]), int(token[1]), int(token[2]), int(token[3]))


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
        keys = [parse_key(data[idx + k]) for k in range(n)]
        idx += n
        out.append(str(solve(keys)))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
