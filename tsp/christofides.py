import networkx as nx

def christofides(G, weight="weight"):

    # cria a minimum spannig tree
    MST = nx.minimum_spanning_tree(G, weight=weight) 

    # faz uma cópia do grafo original e remove as arestas pares da mst
    I = G.copy()
    I.remove_nodes_from([v for v, degree in MST.degree if not (degree % 2)])

    # encontra aparelhamento de peso mínimo do grafo com mst par removido 
    M = nx.min_weight_matching(I, weight=weight)

    # cria um multigrafo com as arestas do mst
    MG = nx.MultiGraph()
    MG.add_edges_from(MST.edges)

    # adiciona arestas do emparelhamento no multigrafo mg
    MG.add_edges_from(M)

    # computa circuito euleriano
    eulerian_circuit = list(nx.dfs_preorder_nodes(MG))
    print(eulerian_circuit)
    print("len:", len(eulerian_circuit))

    # elimina vértices duplicados
    circuit = shortcutting(eulerian_circuit)
    # print(circuit)
    # print("len:", len(circuit))

    # calcula custo final do circuito
    cost = sum(G[u][v][weight] for u, v in zip(circuit, circuit[1:]))
    # print("cost:", cost)
    
    return cost

# método para a remoção de duplicadas
def shortcutting(circuit):
    nodes = []

    for v in circuit:
        if v in nodes:
            continue
        nodes.append(v)

    nodes.append(nodes[0])
    return nodes