import networkx as nx
import random
import matplotlib.pyplot as plt

# question 3

# def check_balance(G):
#     positive_edges_G = G.copy()
#     negative_edges_lst = []
#     for edge in positive_edges_G.edges:
#         if edge['label'] == '-':
#             G.remove_edge(edge[0], edge[1])
#             negative_edges_lst.append(edge)
#     connected_components = nx.connected_components(positive_edges_G)
#     for cc in connected_components:
#         for edge in negative_edges_lst:
#             if edge[0] in cc and edge[1] in cc:
#                 return False
#     super_node_G = G.snap_aggregation
#
#         if
#             (u, v)
#             for (u, v, d) in G.edges(data=True) if d['label'] == '+'

def add_labels_to_graph(prob_for_positive):
    G = nx.erdos_renyi_graph(10, 0.4)

    plus_edges = []
    minus_edges = []
    for (u,v,edge) in G.edges(data=True):
        rnd = random.random()
        if rnd < prob_for_positive:
            edge['label'] = '+'
            plus_edges.append(edge)
        else:
            edge['label'] = '-'
            minus_edges.append(edge)
    return G, plus_edges, minus_edges


G1, plus_edges_1, minus_edges_1 = add_labels_to_graph(0.95)
G2, plus_edges_2, minus_edges_2 = add_labels_to_graph(0.05)




def draw_labeled_graph(G, plus_edges, minus_edges):
    pos = nx.random_layout(G, center=None, dim=2, seed=None)
    # print(G.edges)
    # print(pos)

    # for p in pos:
    #     pos[p] = (pos[p][0], pos[p][1])
    # print(pos)
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=700, node_color='orange')
    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=plus_edges, width=2, edge_color='g')
    nx.draw_networkx_edges(G, pos, edgelist=minus_edges, width=3,
                           alpha=0.5, edge_color='b', arrows=False, style='dashed')
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=18, font_family='sans-serif')

    # Draw edge labels
    edge_labels = dict([((u, v), d['label']) for u, v, d in G.edges(data=True)])
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.axis('off')
    plt.savefig("communication_authority_graph.pdf", format='pdf')  # save as eps
    plt.show()  # display

draw_labeled_graph(G1, plus_edges_1, minus_edges_1)
draw_labeled_graph(G2, plus_edges_2, minus_edges_2)
