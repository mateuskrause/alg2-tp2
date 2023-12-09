import networkx as nx

def twice(G, weight="weight"):

    # cria a minimum spannig tree
    MST = nx.minimum_spanning_tree(G, weight=weight) 

    # computa circuito euleriano
    eulerian_circuit = list(nx.dfs_preorder_nodes(MST))
    # volta para o vértice inicial (1)
    eulerian_circuit.append(1)
    # print(eulerian_circuit)
    # print("len:", len(eulerian_circuit))

    # print(eulerian_circuit)
    # print(circuit)
    # print("len:", len(circuit))

    # calcula custo final do circuito
    cost = sum(G[u][v][weight] for u, v in zip(eulerian_circuit, eulerian_circuit[1:]))
    # print("cost:", cost)
    
    return cost