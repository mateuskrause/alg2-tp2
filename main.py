import networkx as nx
import numpy as np
import pandas as pd
import math
import time
import resource 
import tracemalloc
from datetime import datetime

from tsp import christofides as c
from tsp import twice_around as t
from tsp import branch_and_bound as b

def main():

    """
    código de quais algoritmos serão computados dado o arquivo padrão de datasets

    2 - christofides
    3 - twice around the tree
    5 - branch and bound

    para executar mais de um ao mesmo tempo (e aproveitar o grafo já criado na memoria)
    usar a multiplicação dos algoritmos.

    ex: christofides e twice: 2*3 = 6
    ex: christofides, twice e branch: 2*3*5 = 30
    """

    code = 5
    path = "tp2_datasets.txt"

    tests = pd.read_csv(path, delimiter='\t')

    # novos arquivos para armazenar resultados
    categories = ['Dataset', 'Limiar', 'Cost', 'Quality', 'Time', 'Memory']

    df_2_name = "experiments/christofides-" + str(datetime.now()) + ".csv"
    df_2 = pd.DataFrame(columns=categories)

    df_3_name = "experiments/twice_around-" + str(datetime.now()) + ".csv"
    df_3 = pd.DataFrame(columns=categories)

    df_5_name = "experiments/branch_and_bound-" + str(datetime.now()) + ".csv"
    df_5 = pd.DataFrame(columns=categories)

    if not (code % 2):
        df_2.to_csv(df_2_name, index=False)
        
    if not (code % 3):
        df_3.to_csv(df_3_name, index=False)

    if not (code % 5):
        df_5.to_csv(df_5_name, index=False)

    for index, row in tests.iterrows():
        dataset = row['Dataset']
        limiar = row['Limiar']

        # executa o algoritmo
        answer = tsp(dataset, code)
              
        # apresenta os resultados
        if not (code % 2):
            print(f'C - Dataset: {dataset}, Limiar: {limiar}, Cost: {round(answer[0][0], 2)}, Quality: {round(get_quality(limiar, answer[0][0]), 2)}, Time: {round(answer[0][1], 2)}s, Mem: {round(answer[0][2], 2)}MB')
            row = {'Dataset': dataset, 'Limiar': limiar, 'Cost': round(answer[0][0], 2), 'Quality': round(get_quality(limiar, answer[0][0]), 2), 'Time': round(answer[0][1], 2), 'Memory':round(answer[0][2], 2)}
            result_df = pd.DataFrame([row])
            result_df.to_csv(df_2_name, mode='a', index=False, header=False)
        
        if not (code % 3):
            print(f'T - Dataset: {dataset}, Limiar: {limiar}, Cost: {round(answer[1][0], 2)}, Quality: {round(get_quality(limiar, answer[1][0]), 2)}, Time: {round(answer[1][1], 2)}s, Mem: {round(answer[1][2], 2)}MB')
            row = {'Dataset': dataset, 'Limiar': limiar, 'Cost': round(answer[1][0], 2), 'Quality': round(get_quality(limiar, answer[1][0]), 2), 'Time': round(answer[1][1], 2), 'Memory':round(answer[1][2], 2)}
            result_df = pd.DataFrame([row])
            result_df.to_csv(df_3_name, mode='a', index=False, header=False)

        if not (code % 5):
            print(f'B - Dataset: {dataset}, Limiar: {limiar}, Cost: {round(answer[2][0], 2)}, Quality: {round(get_quality(limiar, answer[2][0]), 2)}, Time: {round(answer[2][1], 2)}s, Mem: {round(answer[2][2], 2)}MB')
            row = {'Dataset': dataset, 'Limiar': limiar, 'Cost': round(answer[2][0], 2), 'Quality': round(get_quality(limiar, answer[2][0]), 2), 'Time': round(answer[2][1], 2), 'Memory':round(answer[2][2], 2)}
            result_df = pd.DataFrame([row])
            result_df.to_csv(df_5_name, mode='a', index=False, header=False)

def get_quality(limiar, cost):
    quality = 0

    limiar = str(limiar)
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
    print("running:", file_path)

    # começa a contagem de tempo e memoria para criação do grafo
    start_time = time.perf_counter()
    tracemalloc.reset_peak()
    tracemalloc.start()

    node_attributes = read_nodes_from_file(file_path)
    G.add_nodes_from(node_attributes.items())

    nodes = list(G.nodes())
    num_nodes = len(nodes)

    # adiciona arestas no grafo
    for i in range(num_nodes):
        for j in range(i + 1, num_nodes):
            pos_i = G.nodes[nodes[i]]["pos"]
            pos_j = G.nodes[nodes[j]]["pos"]
            distance = euclidean_distance(pos_i, pos_j)
            G.add_edge(nodes[i], nodes[j], weight=distance)

    # para a contagem
    end_time = time.perf_counter()
    graph_build_time = end_time - start_time
    current_mem, peak_mem = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    answer = [[], [], []]
    chris_time = 0
    twice_time = 0
    branch_time = 0

    if not (algorithm % 2):
        start_time = time.perf_counter()
        tracemalloc.reset_peak()
        tracemalloc.start()

        # roda algoritmo de christofides
        chris = c.christofides(G)

        end_time = time.perf_counter()
        chris_time = (end_time - start_time) + graph_build_time
        chris_current_mem, chris_peak_mem = tracemalloc.get_traced_memory()
        total_mem = (chris_peak_mem + peak_mem) / (1024 ** 2)
        tracemalloc.stop()
        answer[0] = [math.ceil(chris), chris_time, total_mem]

    if not (algorithm % 3):
        start_time = time.perf_counter()
        tracemalloc.reset_peak()
        tracemalloc.start()

        # roda algoritmo twice around
        twice = t.twice(G)

        end_time = time.perf_counter()
        twice_time = (end_time - start_time) + graph_build_time
        twice_current_mem, twice_peak_mem = tracemalloc.get_traced_memory()
        total_mem = (twice_peak_mem + peak_mem) / (1024 ** 2)
        tracemalloc.stop()
        answer[1] = [math.ceil(twice), twice_time, total_mem]

    if not (algorithm % 5):
        start_time = time.perf_counter()
        tracemalloc.reset_peak()
        tracemalloc.start()

        # roda algoritmo branch and bound
        branch = b.branch_and_bound(G)

        end_time = time.perf_counter()
        branch_time = (end_time - start_time) + graph_build_time
        branch_current_mem, branch_peak_mem = tracemalloc.get_traced_memory()
        total_mem = (branch_peak_mem + peak_mem) / (1024 ** 2)
        tracemalloc.stop()
        answer[2] = [math.ceil(branch), branch_time, total_mem]

    return answer

def read_nodes_from_file(file_path):
    nodes = {}
    data_section = False
    
    # lê o arquivo de datasets
    with open(file_path, 'r') as file:
         for line_number, line in enumerate(file, start=1):

            if "NODE_COORD_SECTION" in line:
                data_section = True
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