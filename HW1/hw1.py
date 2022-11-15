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


# G = (erdos_renyi_model(40,0.1))
# print(nx.average_clustering(G))
# print(clustering_coefficient(G))

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


# def find_top_5(G):
#
#     x = Closeness_centrality(G)
#     closness = [(key,x[key]) for key in x]
#     closness.sort(key= lambda x: x[1], reverse= True)
#     print("top 5 in closness_centrality: ", [closness[i][0] for i in range(5)])
#     x = nx.closeness_centrality(G)
#     closness = [(key, x[key]) for key in x]
#     closness.sort(key=lambda x: x[1], reverse=True)
#     print("top 5 in closness_centrality_nx: ", [closness[i][0] for i in range(5)])
#
#     x = Degree_centrality(G)
#     Degree = [(key, x[key]) for key in x]
#     Degree.sort(key=lambda x: x[1], reverse=True)
#     print("top 5 in Degree_centrality: ", [Degree[i][0] for i in range(5)])
#     x = nx.degree_centrality(G)
#     Degree = [(key, x[key]) for key in x]
#     Degree.sort(key=lambda x: x[1], reverse=True)
#     print("top 5 in Degree_centrality_nx: ", [Degree[i][0] for i in range(5)])
#
#     x = Betweenness_centrality(G)
#     Betweenness = [(key, x[key]) for key in x]
#     Betweenness.sort(key=lambda x: x[1], reverse=True)
#     print("top 5 in betweeness_centrality: ", [Betweenness[i][0] for i in range(5)])
#     x = nx.betweenness_centrality(G)
#     Betweenness = [(key, x[key]) for key in x]
#     Betweenness.sort(key=lambda x: x[1], reverse=True)
#     print("top 5 in betweeness_centrality_nx: ", [Betweenness[i][0] for i in range(5)])

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


G = (nx.gnp_random_graph(15,0.5))
find_top_5(G)
plot_graph(G)

# print(nx.degree_centrality(G))
# print(Degree_centrality(G))
# print(Degree_centrality(G) == nx.degree_centrality(G))
# print(Closeness_centrality(G))
# print(nx.closeness_centrality(G))
# print(Closeness_centrality(G)== nx.closeness_centrality(G))
# print(nx.betweenness_centrality(G))
# x = Betweenness_centrality(G)
# y = nx.betweenness_centrality(G)
# for i in range(1,41):
#     print(abs(x[i]-y[i]))
# print(Betweenness_centrality(G)==nx.betweenness_centrality(G))


# Q3
# a - check balacne

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

# b - add signed labels
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


# G1, plus_edges_1, minus_edges_1 = add_labels_to_graph(0.95)
# G2, plus_edges_2, minus_edges_2 = add_labels_to_graph(0.05)
# print(check_balance(G1))

# c - draw labeles graphs
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

# draw_labeled_graph(G1, plus_edges_1, minus_edges_1)
# draw_labeled_graph(G2, plus_edges_2, minus_edges_2)
