import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

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
    print(circuit)
    print("len:", len(circuit))

    # calcula custo final do circuito
    cost = sum(G[u][v][weight] for u, v in zip(circuit, circuit[1:]))
    print("cost:", cost)
    
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



def main():

    G = nx.Graph()

    def read_nodes_from_file(file_path):
        nodes = {}
        with open(file_path, 'r') as file:
            for line in file:
                parts = line.split()
                node_id = int(parts[0])
                x, y = map(float, parts[1:])
                nodes[node_id] = {"pos": (x, y)}
        return nodes

    file_path = "graph.txt"
    node_attributes = read_nodes_from_file(file_path)
    G.add_nodes_from(node_attributes.items())

    # Define a function to calculate Euclidean distance
    def euclidean_distance(pos1, pos2):
        return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    # Calculate the Euclidean distances and create a distance matrix
    nodes = list(G.nodes())
    num_nodes = len(nodes)

    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            pos_i = G.nodes[nodes[i]]["pos"]
            pos_j = G.nodes[nodes[j]]["pos"]
            distance = euclidean_distance(pos_i, pos_j)
            G.add_edge(nodes[i], nodes[j], weight=distance)

    # Print the edges with weights
    # for edge in G.edges(data=True):
    #     print(f"Edge {edge[0]} - {edge[1]}: Weight {edge[2]['weight']}")

    # print(list(G.nodes))
    # print(list(G.edges))

    # ----------------------------------
    print("christofides: ", christofides(G, "weight"))
    # ----------------------------------

    # draw graph
    node_positions = {node: data["pos"] for node, data in G.nodes(data=True)}
    edge_weights = {(edge[0], edge[1]): edge[2]['weight'] for edge in G.edges(data=True)}
    nx.draw(G, pos=node_positions, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", edge_color="gray", linewidths=1, width=2)
    nx.draw_networkx_edge_labels(G, pos=node_positions, edge_labels=edge_weights, font_color='red')
    plt.show()



if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()