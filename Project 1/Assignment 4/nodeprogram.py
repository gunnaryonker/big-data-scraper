import csv
import networkx as nx
import matplotlib.pyplot as plt

def read_csv_file(filename):
    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        graph = nx.DiGraph()
        for row in reader:
            parent_node = row[0].strip()
            child_nodes = [child.strip() for child in row[1:]]
            graph.add_node(parent_node)
            for child_node in child_nodes:
                graph.add_edge(parent_node, child_node)
        return graph

def calculate_pagerank(graph):
    pagerank = nx.pagerank(graph)
    return pagerank

def draw_graph(graph, pagerank):
    levels = {node: 1 for node in graph.nodes()}
    max_level = 1
    
    for node in graph.nodes():
        in_degree = graph.in_degree(node)
        if in_degree > 0:
            parent_level = max(levels[parent] for parent in graph.predecessors(node))
            levels[node] = parent_level + 1
            max_level = max(max_level, parent_level + 1)

    pos = {}
    for level in range(1, max_level + 1):
        level_nodes = [node for node in graph.nodes() if levels[node] == level]
        pos.update((node, (i, max_level - level + 1)) for i, node in enumerate(level_nodes))
    
    # Calculate the x-coordinate for Node2 as the midpoint of Node4 and Node5
    parent_nodes = [node for node in graph.nodes() if graph.in_degree(node) == 0]
    if parent_nodes:
        parent_node = parent_nodes[0]
        child_nodes = [node for node in graph.successors(parent_node)]
        
        # Calculate the midpoint between Node4 and Node5
        x4, _ = pos[child_nodes[0]]
        x5, _ = pos[child_nodes[1]]
        center_x = (x4 + x5) / 2.0
        pos[parent_node] = (center_x, max_level + 1)
    
    node_sizes = [pagerank[node] * 3000 for node in graph.nodes()]
    
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(graph, pos, node_size=node_sizes, node_color='b', alpha=0.6)
    nx.draw_networkx_labels(graph, pos, font_size=12, font_color='k', font_weight='bold')
    nx.draw_networkx_edges(graph, pos, edge_color='grey', arrows=True, width=1.0, alpha=0.6)
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    csv_file = "graph.csv"
    graph = read_csv_file(csv_file)
    pagerank = calculate_pagerank(graph)
    draw_graph(graph, pagerank)
