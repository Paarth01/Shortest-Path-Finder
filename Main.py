import tkinter as tk
from tkinter import messagebox
import heapq
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

def heuristic(a, b):
    return abs(ord(a) - ord(b))  # Simple heuristic for demo

def a_star(graph, start, goal):
    pq = [(0, start)]
    came_from = {}
    g_score = {node: float('inf') for node in graph}
    g_score[start] = 0
    
    while pq:
        _, current = heapq.heappop(pq)
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for neighbor, weight in graph[current].items():
            temp_g_score = g_score[current] + weight
            if temp_g_score < g_score[neighbor]:
                g_score[neighbor] = temp_g_score
                f_score = temp_g_score + heuristic(neighbor, goal)
                heapq.heappush(pq, (f_score, neighbor))
                came_from[neighbor] = current
    
    return None  # No path found

def find_shortest_path():
    start = start_entry.get().strip()
    goal = goal_entry.get().strip()
    
    if start not in graph or goal not in graph:
        messagebox.showerror("Error", "Start or Goal node not found in graph!")
        return
    
    path = a_star(graph, start, goal)
    if path:
        result_label.config(text=f"Shortest Path: {' → '.join(path)}")
    else:
        result_label.config(text="No path found")
    update_graph(path)

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
    graph[node2][node1] = weight  # Assuming an undirected graph
    
    messagebox.showinfo("Success", f"Edge added: {node1} --{weight}--> {node2}")
    update_graph()

def update_graph(path=None):
    G.clear()
    for node in graph:
        G.add_node(node)
    for node, neighbors in graph.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)
    
    plt.clf()
    pos = nx.spring_layout(G)
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2000, font_size=10)
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

tk.Button(frame, text="Add Edge", command=add_edge).grid(row=3, columnspan=2)

tk.Label(frame, text="Start Node:").grid(row=4, column=0)
start_entry = tk.Entry(frame)
start_entry.grid(row=4, column=1)

tk.Label(frame, text="Goal Node:").grid(row=5, column=0)
goal_entry = tk.Entry(frame)
goal_entry.grid(row=5, column=1)

tk.Button(frame, text="Find Shortest Path", command=find_shortest_path).grid(row=6, columnspan=2)

result_label = tk.Label(frame, text="")
result_label.grid(row=7, columnspan=2)

fig, ax = plt.subplots(figsize=(5, 4))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
update_graph()

root.mainloop()