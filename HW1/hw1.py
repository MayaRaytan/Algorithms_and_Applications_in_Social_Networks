import networkx as nx
import random
import matplotlib.pyplot as plt
import pandas as pd


# question 3

def check_balance(G):

    positive_edges_G = G.copy()
    negative_edges_lst = []
    for (u, v, d) in G.edges(data=True):
        if d['label'] == '-':
            positive_edges_G.remove_edge(u, v)
            negative_edges_lst.append((u,v))
    super_node_G = nx.Graph()
    connected_components = nx.connected_components(positive_edges_G)
    i = 0
    node_to_super_node = {}
    for cc in connected_components:
        for node in cc:
            node_to_super_node[node] = i
        i += 1
        for edge in negative_edges_lst:
            if edge[0] in cc and edge[1] in cc:
                return False
    for edge in negative_edges_lst:
        super_node_G.add_edge(node_to_super_node[edge[0]], node_to_super_node[edge[1]])

    return nx.algorithms.bipartite.is_bipartite(super_node_G)


def add_labels_to_graph(prob_for_positive):
    G = nx.erdos_renyi_graph(10, 0.4)
    plus_edges = []
    minus_edges = []
    for (u,v,edge) in G.edges(data=True):
        rnd = random.random()
        if rnd < prob_for_positive:
            edge['label'] = '+'
            plus_edges.append((u,v))
        else:
            edge['label'] = '-'
            minus_edges.append((u,v))
    return G, plus_edges, minus_edges


G1, plus_edges_1, minus_edges_1 = add_labels_to_graph(0.95)
G2, plus_edges_2, minus_edges_2 = add_labels_to_graph(0.05)
print(check_balance(G1))


def draw_labeled_graph(G, plus_edges, minus_edges):
    pos = nx.spring_layout(G)
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, nodelist=[node for node in nx.nodes(G)], node_color='orange')
    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=plus_edges, width=2, edge_color='g')
    nx.draw_networkx_edges(G, pos, edgelist=minus_edges, width=3, edge_color='b')
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=18, font_family='sans-serif')
    # Draw edge labels
    edge_labels = dict([((u, v), d['label']) for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.savefig("q3di.pdf", format='pdf')  # save as eps
    plt.show()  # display

draw_labeled_graph(G1, plus_edges_1, minus_edges_1)
# draw_labeled_graph(G2, plus_edges_2, minus_edges_2)
