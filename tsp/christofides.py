import networkx as nx

def christofides(G, weight="weight"):

    # cria a minimum spannig tree e remove as arestas pares
    MST = nx.minimum_spanning_tree(G, weight=weight) 
    I = G.copy()

    nodes_to_remove = []
    for v, degree in MST.degree:
        if not degree % 2:
            nodes_to_remove.append(v)

    I.remove_nodes_from(nodes_to_remove)

    # encontra aparelhamento de peso mínimo do grafo com mst par removido 
    M = nx.min_weight_matching(I, weight=weight)

    # cria um multigrafo com as arestas da mst e adiciona arestas do emparelhamento
    MG = nx.MultiGraph()
    MG.add_edges_from(MST.edges)
    MG.add_edges_from(M)

    # computa circuito euleriano elimina vertices duplicados
    eulerian_circuit = list(nx.dfs_preorder_nodes(MG))
    circuit = shortcutting(eulerian_circuit)

    # calcula custo final do circuito
    cost = sum(G[u][v][weight] for u, v in zip(circuit, circuit[1:]))
    
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