import networkx as nx

def twice(G, weight="weight"):

    # cria a minimum spannig tree
    MST = nx.minimum_spanning_tree(G, weight=weight) 

    # computa circuito euleriano e adiciona a volta ao início
    eulerian_circuit = list(nx.dfs_preorder_nodes(MST))
    eulerian_circuit.append(1)

    # calcula custo final do circuito
    cost = sum(G[u][v][weight] for u, v in zip(eulerian_circuit, eulerian_circuit[1:]))
 
    return cost