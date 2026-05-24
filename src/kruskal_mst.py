"""
Kruskal: arvore geradora minima de um grafo nao-direcionado
com pesos nas arestas.

Recebe:
    n_vertices    - numero de vertices (rotulados 0..n-1)
    edges         - lista de objetos Edge

Algoritmo:
    1. Ordena as arestas por peso crescente.
    2. Percorre as arestas em ordem, usando Union-Find para
       evitar ciclos. Inclui a aresta se conecta componentes
       diferentes. Para quando a MST tem n-1 arestas.

Complexidade: O(E log E) pela ordenacao, mais O(E alfa(V))
pelas operacoes de Union-Find (praticamente lineares).

Baseado conceitualmente em algs4-py/algs4/kruskal_mst.py.
"""

from uf import UF


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

    def edges(self):
        return self.mst
