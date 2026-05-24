"""
Aresta de grafo nao-direcionado com peso inteiro.

Baseado conceitualmente em algs4-py/algs4/edge.py, com peso
inteiro pois as distancias deste problema sao inteiras (0..20).
"""


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

    def __repr__(self):
        return "%d-%d %d" % (self.v, self.w, self.weight)
