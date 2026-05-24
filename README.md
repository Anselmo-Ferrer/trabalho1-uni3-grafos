# Trabalho Prático 1 — Unidade 3 — Grupo F

**Disciplina:** Resolução de Problemas com Grafos
**Orientador:** Prof. Me Ricardo Carubbi

---

## Nome do problema

**UVA 1235 — Anti Brute Force Lock**

## Link do problema

<https://uva.onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=3676>

## Integrantes do grupo

| Nome | Matrícula |
| --- | --- |
| Anselmo Teixeira | 2410414 |
| João Marcelo Jucá | 2410392 |
| Thiago Victor Ferreira | 2410413 |

## Linguagem utilizada

Python 3 (testado com Python 3.10+). Apenas a biblioteca padrão (`sys`) — nenhuma dependência externa.

## Como executar a solução

Toda execução é feita a partir da pasta `src/`. A entrada é lida via *stdin*, igual ao juiz do UVA faz.

### Rodando a versão modular (com módulos `edge.py`, `uf.py`, `kruskal_mst.py`)

```sh
cd src
python3 main.py < ../dados/entradas_do_problema.txt
```

### Rodando a versão de submissão (arquivo único enviado ao UVA)

```sh
cd src
python3 submissao_uva.py < ../dados/entradas_do_problema.txt
```

### Saída esperada para o arquivo de exemplo (4 casos do enunciado)

```text
16
20
26
17
```

A saída produzida localmente está salva em [`evidencias/saida_local.txt`](evidencias/saida_local.txt) e bate exatamente com a saída esperada.

---

## Explicação da modelagem do problema como grafo ponderado

### Resumo do problema

Um cadeado tem 4 dígitos, cada um circular (gira de 0 a 9 com 9↔0). Cada giro custa 1. Existem até `N ≤ 500` chaves que precisam ser todas desbloqueadas. O cadeado começa em `0000` e o botão **JUMP** teletransporta de graça para qualquer chave **já desbloqueada** — mas **não** para o `0000` (que não é uma chave desbloqueada). Queremos o **mínimo de giros** para abrir todas as chaves.

### Grafo ponderado

- **Vértices:** cada chave de 4 dígitos é um vértice. Não modelamos o `0000` como vértice — ele é tratado separadamente (ver mais abaixo, "Variação de MST").
- **Arestas:** grafo **completo** entre as chaves (uma aresta para cada par).
- **Peso da aresta `(a, b)`:** quantidade mínima de giros para transformar a chave `a` na chave `b`. Como cada dígito é circular:

  ```
  dist_digito(x, y) = min( |x - y| , 10 - |x - y| )
  w(a, b) = soma_{i = 0..3} dist_digito(a[i], b[i])
  ```

  Exemplo: `w(1155, 2211) = 1 + 1 + 4 + 4 = 10`.

A função `key_distance` no [`src/main.py`](src/main.py) calcula esse peso usando uma tabela pré-computada `DIGIT_DIST[10][10]` (cálculo O(1) por aresta).

### Por que a modelagem funciona

Depois de desbloquear a primeira chave, qualquer chave nova pode ser alcançada partindo da chave aberta **mais barata** (JUMP é grátis até ela). Esse comportamento é exatamente como uma **árvore geradora mínima** se constrói: cada novo vértice é conectado pela aresta mais leve possível ao já conectado.

---

## Algoritmo utilizado

**Kruskal** para a árvore geradora mínima, com **Union-Find (DSU)** por tamanho e compressão de caminho.

### Por que Kruskal e não Prim

O grafo é **denso** (completo entre as chaves), mas `N ≤ 500` resulta em ~125 mil arestas no pior caso. Ordenar essa lista é barato (`O(E log E)`), e Kruskal com Union-Find evita a necessidade de uma fila de prioridade indexada que o Prim eficiente em grafo denso exige. O código fica mais simples de escrever, ler e explicar.

### Etapas do Kruskal (em [`src/kruskal_mst.py`](src/kruskal_mst.py))

1. Ordenar todas as arestas por peso crescente.
2. Percorrer em ordem; para cada aresta `(v, w)`:
   - se `v` e `w` **já estão** no mesmo componente do Union-Find → pular (formaria ciclo);
   - senão → unir os componentes (`uf.union`) e adicionar a aresta à MST.
3. Parar quando a MST tiver `N - 1` arestas.

---

## Papel do Union-Find/DSU

O Union-Find é o que permite o Kruskal rodar em quase tempo linear. Ele responde duas perguntas em praticamente `O(1)`:

- `find(p)` — retorna a "raiz" do componente conectado de `p`;
- `connected(p, q)` — verifica se `p` e `q` estão no mesmo componente (basta comparar as raízes);
- `union(p, q)` — funde os componentes de `p` e `q`.

No Kruskal, antes de aceitar uma aresta `(v, w)`, perguntamos `uf.connected(v, w)`. Se a resposta for `True`, adicionar essa aresta criaria um **ciclo** — e MST por definição não tem ciclo. Sem o Union-Find, essa verificação levaria `O(V + E)` por aresta (uma busca em grafo), tornando o Kruskal inviável.

Nossas duas otimizações clássicas, em [`src/uf.py`](src/uf.py):

- **Union por tamanho:** ao unir dois componentes, o menor é pendurado sob o maior, mantendo as árvores rasas.
- **Compressão de caminho:** durante o `find`, cada nó visitado é repontado direto pra raiz, achatando a árvore.

Combinadas, dão complexidade amortizada de `O(α(N))` por operação (`α` é a inversa de Ackermann, `≤ 4` para qualquer `N` prático).

---

## Variação de MST usada

Este problema **não** é uma MST clássica pura — tem uma variação importante: o cadeado começa em `0000`, mas `0000` **não é uma chave desbloqueada**, então o JUMP nunca volta para lá de graça.

Se tratássemos `0000` como vértice comum, a MST poderia conectar várias chaves diretamente a ele (grau > 1) — implicando "voltar de graça" ao `0000`, o que o problema proíbe.

**Nossa solução:** decompor o problema em duas partes:

1. **MST somente entre as chaves** (sem o `0000`).
2. **Mais a aresta da primeira saída** de `0000`, que pela escolha ótima é a chave mais próxima de `0000`.

### Justificativa

Para qualquer ordem de desbloqueio `k_{π(1)}, k_{π(2)}, …, k_{π(N)}`:

- Custo da primeira chave: `dist(0000, k_{π(1)})`.
- Custo de cada chave `i > 1`: `min_{j < i} dist(k_{π(j)}, k_{π(i)})` (JUMP grátis até a chave aberta mais barata).

O segundo somatório, sobre todas as escolhas possíveis, define uma árvore geradora sobre as chaves, e o mínimo é a **MST**. Como o peso da MST não depende da raiz, o mínimo global é:

```
resposta = MST(chaves) + min_{k em chaves} dist(0000, k)
```

A escolha "começar pela chave mais próxima de `0000`" é factível e atinge esse mínimo.

### Verificação numérica (caso 3 do enunciado)

Chaves `1234`, `5678`, `9090`. Distâncias entre pares: `w(1234, 9090) = 12`, `w(5678, 9090) = 12`, `w(1234, 5678) = 16`. MST = `12 + 12 = 24`. Distância mínima de `0000` às chaves: `dist(0000, 9090) = 2`. Resposta: `24 + 2 = 26` ✅ (bate com o enunciado).

---

## Análise de complexidade

Seja `N` o número de chaves no caso de teste (`N ≤ 500`).

| Etapa | Custo |
| --- | --- |
| Construção das arestas (grafo completo) | `O(N²)` arestas |
| Cálculo de cada peso (com tabela `DIGIT_DIST`) | `O(1)` por aresta |
| Ordenação das arestas pelo Kruskal | **`O(N² log N)`** (dominante) |
| Kruskal com Union-Find | `O(N² · α(N))` ≈ linear |
| Cálculo de `min dist(0000, k)` | `O(N)` |

**Complexidade de tempo por caso:** `O(N² log N)`.
**Memória dominante:** lista de arestas, `O(N²)`.

Para `N = 500`, são ~125 mil arestas. A submissão aceita no UVA rodou em **1.950 s** (PYTH3), bem dentro do limite.

---

## Casos especiais relevantes

- **`N = 1`** — só uma chave. Não há MST a construir; a resposta é apenas `dist(0000, k)`. O código trata explicitamente esse caso em [`src/main.py`](src/main.py).
- **Chave igual a `0000` na entrada** — `dist(0000, k) = 0`, então `min dist(0000, k) = 0` e o programa não paga giros extras pela primeira saída.
- **Chaves duplicadas na entrada** — produzem arestas de peso 0; o Kruskal as absorve sem afetar o resultado (ele as une de graça).
- **Distância máxima de um dígito = 5** — `min(5, 5) = 5`. Tanto faz girar pra cima ou pra baixo. Já é coberto pela fórmula `min(|x-y|, 10-|x-y|)`.
- **Grafo sempre conexo** — como cada par de chaves tem uma aresta (grafo completo), nunca há problema de desconexão. A MST sempre existe.
- **Pesos iguais** — comum (muitos pares têm o mesmo peso); o Kruskal aceita qualquer ordem de desempate sem afetar a corretude do peso total da MST.

---

## Evidência de Accepted

Submissão aceita no UVA Online Judge:

| Campo | Valor |
| --- | --- |
| Submission ID | 31141305 |
| Problema | 1235 — Anti Brute Force Lock |
| Verdict | **Accepted** |
| Linguagem | PYTH3 |
| Run Time | 1.950 s |
| Data | 2026-05-22 |

Print do veredito: [`evidencias/accepted.png`](evidencias/accepted.png).
Saída local nos exemplos do enunciado: [`evidencias/saida_local.txt`](evidencias/saida_local.txt).

---

## Estrutura do repositório

```text
projeto/
├── README.md
├── src/
│   ├── main.py             # leitura, modelagem, orquestração
│   ├── edge.py             # classe Edge (espelha algs4-py/edge.py)
│   ├── uf.py               # Union-Find/DSU (espelha algs4-py/uf.py)
│   ├── kruskal_mst.py      # Kruskal (espelha algs4-py/kruskal_mst.py)
│   └── submissao_uva.py    # versão de arquivo único enviada ao UVA
├── dados/
│   └── entradas_do_problema.txt   # 4 casos do enunciado
├── evidencias/
│   ├── accepted.png        # print do Accepted no UVA
│   └── saida_local.txt     # saída do programa nos exemplos
└── apresentacao/
    └── apresentacao.pdf    # slides da apresentação em sala
```

> A versão modular (`main.py` + módulos) segue a estrutura exigida pelo
> trabalho e a referência conceitual do `algs4-py`. Como o juiz do UVA
> compila **um único arquivo**, a mesma lógica está reunida em
> `submissao_uva.py`, que foi o arquivo de fato submetido.

## Referência conceitual

A organização dos módulos espelha a base **`algs4-py`** (versão Python do livro *Algorithms, 4th Edition* de Sedgewick & Wayne), citada como referência no enunciado do trabalho:

- `Edge` ↔ `algs4-py/algs4/edge.py` (mesmos atributos `v`, `w`, `weight`; mesmos métodos `either()`, `other(v)`, `__lt__`).
- `UF` ↔ `algs4-py/algs4/uf.py` (mesmo `find` com compressão de caminho e `union` por tamanho).
- `KruskalMST` ↔ `algs4-py/algs4/kruskal_mst.py` (mesmo padrão: ordena arestas, percorre, descarta as que formam ciclo via Union-Find).

Trocamos o `MinPQ` do `algs4-py` por `sorted(edges)` da biblioteca padrão (ambas dão `O(E log E)`), conforme permitido pelo enunciado ("ordenação padrão pode ser usada como apoio"). Nenhuma biblioteca externa de grafos ou MST pronta foi utilizada — Kruskal e Union-Find foram implementados pelo grupo.
