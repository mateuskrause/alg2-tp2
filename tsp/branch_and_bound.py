import networkx as nx
import heapq
from math import inf

def bound(node, G):
    n = G.number_of_nodes()

    # obtem nao visitados
    vertices =  [i for i in range(1, n + 1)]
    not_visited = set(vertices) - set(node[-1])

    min_in_weight = 0
    min_out_weight = 0

    # se há vertices nao visitados, calcule os pesos das arestas
    if not_visited:

        in_weight = []
        for v in not_visited:
            weight = G[v][node[-1][0]]['weight']
            in_weight.append(weight)

        min_in_weight = min(in_weight)

        out_weight = []
        for v in not_visited:
            weight = G[node[-1][-1]][v]['weight']
            out_weight.append(weight)

        min_out_weight = min(out_weight)        

    return node[0] + min_in_weight + min_out_weight

def branch_and_bound(G):

    n = G.number_of_nodes()
    empty = (0, 1, 0, [1])

    # (limite inferior, numero vertices visitados, custo acumulado, lista vértices visitados)
    root = (bound(empty, G), 1, 0, [1])

    # estado inicial da busca, onde há apenas o nó de início
    queue = [root]
    heapq.heapify(queue)
    best = inf
    sol = []

    # faz a analise até que não tenha mais vértices restantes
    while len(queue) != 0:

        # retira o nó para ser analisado
        node = heapq.heappop(queue)

        # caso o número de vértices visitados seja igual ao número de vértices total
        if node[1] == n:
            weight = G[node[-1][-1]][node[-1][0]]['weight']
            current_cost = node[2] + weight
            best = min(best, current_cost)
            sol = node[3]

        # caso o valor do limiar do nó atual é menor que o melhor resultado conhecido
        elif node[0] < best:

            vertices =  [i for i in range(1, n + 1)]
            remaining = set(vertices) - set(node[-1])

            # calcula proximos nodes e seus valores
            for v in remaining:
                if G.has_edge(node[-1][-1], v):
                    new_visited = node[3] + [v]
                    new_limiar = bound((node[0], node[1] + 1, node[2], new_visited), G)
                    new_node = (new_limiar, node[1] + 1, node[2] + G[node[3][-1]][v]['weight'], new_visited)
                    heapq.heappush(queue, new_node)

    return best