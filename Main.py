import tkinter as tk
from tkinter import messagebox
import heapq
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def dijkstra(graph, start, goal):
    pq = [(0, start)]  # (distance, node)
    came_from = {}
    distances = {node: float('inf') for node in graph}
    distances[start] = 0

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == goal:
            path = []
            while current_node in came_from:
                path.append(current_node)
                current_node = came_from[current_node]
            path.append(start)
            return path[::-1]

        for neighbor, weight in graph[current_node].items():
            new_distance = current_distance + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                heapq.heappush(pq, (new_distance, neighbor))
                came_from[neighbor] = current_node
    
    return None

def find_shortest_path():
    start = start_entry.get().strip()
    goal = goal_entry.get().strip()
    
    if start not in graph or goal not in graph:
        messagebox.showerror("Error", "Start or Goal node not found in graph!")
        return
    
    path = dijkstra(graph, start, goal)
    
    if path:
        result_label.config(text=f"Shortest Path: {' → '.join(path)}")
        update_graph(path)
    else:
        result_label.config(text="No path found")

def add_edge():
    node1 = node1_entry.get().strip()
    node2 = node2_entry.get().strip()
    weight = weight_entry.get().strip()
    
    if not (node1 and node2 and weight.isdigit()):
        messagebox.showerror("Error", "Invalid input")
        return
    
    weight = int(weight)
    if node1 not in graph:
        graph[node1] = {}
    if node2 not in graph:
        graph[node2] = {}
    
    graph[node1][node2] = weight
    
    if not directed_var.get():  # If undirected, add the reverse edge
        graph[node2][node1] = weight
    
    messagebox.showinfo("Success", f"Edge added: {node1} --{weight}--> {node2}")
    update_graph()

def update_graph(path=None):
    global G
    G.clear()
    
    if directed_var.get():
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    
    for node in graph:
        G.add_node(node)
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)
    
    plt.clf()
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10, arrows=directed_var.get())
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2)
    
    canvas.draw()

graph = {}
G = nx.Graph()
root = tk.Tk()
root.title("Interactive Shortest Path Finder")

frame = tk.Frame(root)
frame.pack(side=tk.LEFT, padx=20, pady=20)

tk.Label(frame, text="Node 1:").grid(row=0, column=0)
node1_entry = tk.Entry(frame)
node1_entry.grid(row=0, column=1)

tk.Label(frame, text="Node 2:").grid(row=1, column=0)
node2_entry = tk.Entry(frame)
node2_entry.grid(row=1, column=1)

tk.Label(frame, text="Weight:").grid(row=2, column=0)
weight_entry = tk.Entry(frame)
weight_entry.grid(row=2, column=1)

directed_var = tk.BooleanVar()
directed_checkbox = tk.Checkbutton(frame, text="Directed Graph", variable=directed_var)
directed_checkbox.grid(row=3, columnspan=2)

tk.Button(frame, text="Add Edge", command=add_edge).grid(row=4, columnspan=2)

tk.Label(frame, text="Start Node:").grid(row=5, column=0)
start_entry = tk.Entry(frame)
start_entry.grid(row=5, column=1)

tk.Label(frame, text="Goal Node:").grid(row=6, column=0)
goal_entry = tk.Entry(frame)
goal_entry.grid(row=6, column=1)

tk.Button(frame, text="Find Shortest Path", command=find_shortest_path).grid(row=7, columnspan=2)

result_label = tk.Label(frame, text="")
result_label.grid(row=8, columnspan=2)

fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
update_graph()

root.mainloop()
