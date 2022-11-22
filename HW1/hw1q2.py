import networkx as nx
import random
import collections
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
# Q2
# a - centrality measures
def Degree_centrality(G):
    res = collections.defaultdict(int)
    n = nx.number_of_nodes(G)
    for i in nx.nodes(G):
        res[i] = len([node for node in G.neighbors(i)])/(n-1)
    return res


def Betweenness_centrality(G):
    n = nx.number_of_nodes(G)
    all_nodes = [node for node in nx.nodes(G)]
    helper = dict()
    for u in range(len(all_nodes)):
        for v in range(u+1,len(all_nodes)):
            try:
                x = nx.all_shortest_paths(G, all_nodes[u], all_nodes[v])
                l = 0
                for path in x:
                    for i in range(1,len(path)-1):
                        if path[i] not in helper:
                            helper[path[i]] = [0, 0]
                        helper[path[i]][0] += 1
                    l += 1
                for node in helper:
                    helper[node][0] /= l
                    helper[node][0] /= l
                    helper[node][1] += helper[node][0]
                    helper[node][0] = 0
            except:
                continue
    for node in helper:
        helper[node] = (helper[node][1]*2)/((n-1)*(n-2))
    return helper


def Closeness_centrality(G):
    res = collections.defaultdict(int)
    n = nx.number_of_nodes(G)
    shortest_paths = nx.shortest_path_length(G)
    for node in shortest_paths:
        for key in node[1]:
            res[node[0]] += node[1][key]
        if res[node[0]] != 0:
            res[node[0]] = (n-1)/res[node[0]]
    return res


# b - top-5
def find_top_5(G):
    x = Closeness_centrality(G)
    closness = [(key,x[key]) for key in x]
    closness.sort(key= lambda x: x[1], reverse= True)
    print("top 5 in closness_centrality: ", [closness[i][0] for i in range(5)])

    x = Degree_centrality(G)
    Degree = [(key, x[key]) for key in x]
    Degree.sort(key=lambda x: x[1], reverse=True)
    print("top 5 in Degree_centrality: ", [Degree[i][0] for i in range(5)])

    x = Betweenness_centrality(G)
    Betweenness = [(key, x[key]) for key in x]
    Betweenness.sort(key=lambda x: x[1], reverse=True)
    print("top 5 in betweeness_centrality: ", [Betweenness[i][0] for i in range(5)])


# c - plot graph
def plot_graph(G):
    plt.figure(3,figsize=(26,15))
    Cb = Betweenness_centrality(G)
    Cc = Closeness_centrality(G)
    Cd = Degree_centrality(G)

    pos = nx.spring_layout(G)
    nodes = [node for node in nx.nodes(G)]

    # plot the Degree
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color='violet',node_size=[Cd[node]*2000 for node in nodes])
    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=2, edge_color='black')
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=18, font_family='sans-serif')
    # Draw edge labels
    plt.savefig("Degree_nodes.pdf", format='pdf')  # save as eps
    plt.show()

    # plot the Betweenness
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color='skyblue', node_size=[Cb[node] * 30000 for node in nodes])
    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=2, edge_color='black')
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=18, font_family='sans-serif')
    # Draw edge labels
    plt.savefig("Betweenness_nodes.pdf", format='pdf')  # save as eps
    plt.show()

    # plot the Closeness
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_color='limegreen', node_size=[Cc[node] * 2500 for node in nodes])
    # Draw edges
    nx.draw_networkx_edges(G, pos, edgelist=G.edges, width=2, edge_color='black')
    # Draw node labels
    nx.draw_networkx_labels(G, pos, font_size=18, font_family='sans-serif')
    # Draw edge labels
    plt.savefig("Closeness_nodes.pdf", format='pdf')  # save as eps
    plt.show()
