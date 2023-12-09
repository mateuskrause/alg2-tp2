import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import resource 
import tracemalloc

from tsp import christofides as c
from tsp import twice_around as t

def main():
    code = 3

    path = "tp2_datasets.txt"
    tests = pd.read_csv(path, delimiter='\t')

    for index, row in tests.iterrows():
        dataset = row['Dataset']
        limiar = row['Limiar']

        # executa o algoritmo
        answer = tsp(dataset, code)
              
        if not (code % 2):
            print(f'C - Dataset: {dataset}, Limiar: {limiar}, Cost: {round(answer[0][0], 2)}, Quality: {round(get_quality(limiar, answer[0][0]), 2)}, Time: {round(answer[0][1], 2)}s')
        
        if not (code % 3):
            print(f'T - Dataset: {dataset}, Limiar: {limiar}, Cost: {round(answer[1][0], 2)}, Quality: {round(get_quality(limiar, answer[1][0]), 2)}, Time: {round(answer[1][1], 2)}s')

def get_quality(limiar, cost):
    quality = 0

    if limiar[0] == '[':
        values = limiar[1:-1].split(',')
        range = (values[0], values[1])
        if cost in range:
            quality = 1
        else:
            quality = cost / float(values[0])
    else:
        quality = cost / float(limiar)

    return quality

def tsp(dataset, algorithm=30):
    G = nx.Graph()

    file_path = "datasets/" + dataset + ".tsp"
    print("file_path:", file_path)

    # começa a contagem de tempo para criação do grafo
    start_time = time.perf_counter()

    node_attributes = read_nodes_from_file(file_path)
    G.add_nodes_from(node_attributes.items())

    # Calculate the Euclidean distances and create a distance matrix
    nodes = list(G.nodes())
    num_nodes = len(nodes)

    # adiciona arestas no grafo
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            pos_i = G.nodes[nodes[i]]["pos"]
            pos_j = G.nodes[nodes[j]]["pos"]
            distance = euclidean_distance(pos_i, pos_j)
            G.add_edge(nodes[i], nodes[j], weight=distance)

    # stop the count!
    end_time = time.perf_counter()
    graph_build_time = end_time - start_time

    answer = [[], [], []]
    chris_time = 0
    twice_time = 0
    branch_time = 0

    if not (algorithm % 2):
        start_time = time.perf_counter()

        # roda algoritmo de christofides
        chris = c.christofides(G)

        end_time = time.perf_counter()
        chris_time = (end_time - start_time) + graph_build_time
        answer[0] = [chris, chris_time]

    if not (algorithm % 3):
        start_time = time.perf_counter()

        # roda algoritmo twice around
        twice = t.twice(G)

        end_time = time.perf_counter()
        twice_time = (end_time - start_time) + graph_build_time
        answer[1] = [twice, twice_time]

    if not (algorithm % 5):
        start_time = time.perf_counter()

        # roda algoritmo branch and bound
        print("branch and bound")

        end_time = time.perf_counter()
        branch_time = (end_time - start_time) + graph_build_time
        answer[2] = [0, 0]

    return answer


    # draw graph
    # node_positions = {node: data["pos"] for node, data in G.nodes(data=True)}
    # edge_weights = {(edge[0], edge[1]): edge[2]['weight'] for edge in G.edges(data=True)}
    # nx.draw(G, pos=node_positions, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", edge_color="gray", linewidths=1, width=2)
    # nx.draw_networkx_edge_labels(G, pos=node_positions, edge_labels=edge_weights, font_color='red')
    # plt.show()


def read_nodes_from_file(file_path):
    nodes = {}
    data_section = False
    
    with open(file_path, 'r') as file:
         for line_number, line in enumerate(file, start=1):
            if "NODE_COORD_SECTION" in line:
                data_section = True  # Start processing lines after this line
                continue

            if not data_section:
                continue

            if line == "EOF\n":
                break

            parts = line.split()
            node_id = int(parts[0])
            x, y = map(float, parts[1:])
            nodes[node_id] = {"pos": (x, y)}

    return nodes

def euclidean_distance(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()