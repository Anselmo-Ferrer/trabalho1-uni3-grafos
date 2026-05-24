"""
Union-Find (DSU) com union por tamanho e compressão de caminho.

Baseado conceitualmente em algs4-py/algs4/uf.py.

Operacoes:
    find(p)        - retorna a raiz do componente de p
    union(p, q)    - une os componentes de p e q
    connected(p,q) - True se p e q estao no mesmo componente
"""


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
