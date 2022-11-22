import networkx as nx
import random
import collections
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


# Q1
# a- random erdos-renyi graph
def erdos_renyi_model(n,p):
    G = nx.Graph()
    G.add_nodes_from([i for i in range(1,n+1)])
    for i in range(1,n+1):
        for j in range(i+1,n+1):
            if random.random() < p:
                G.add_edge(i,j)
    return G


# b  - clustering coefficient
def clustering_coefficient_node(G,i):
    neighbors =[neighbor for neighbor in G.neighbors(i)]
    k = len(neighbors)
    exist = 0
    for i in range(k):
        for j in range(i+1,k):
            if G.has_edge(neighbors[i],neighbors[j]):
                exist += 1
    if k <= 1 :
        return 0
    return 2*exist/(k*(k-1))


def clustering_coefficient(G):
    all_coeffs = 0
    for node in nx.nodes(G):
        all_coeffs += clustering_coefficient_node(G,node)
    return all_coeffs/nx.number_of_nodes(G)