import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Title
st.title("🚗 Shortest Route Finder Between Towns")

# Define the graph
G = nx.Graph()

# Add weighted edges (town connections)
edges = [
    ("Origin", "A", 40),
    ("Origin", "B", 60),
    ("Origin", "C", 50),
    ("A", "B", 10),
    ("A", "D", 70),
    ("B", "C", 20),
    ("B", "D", 55),
    ("B", "E", 40),
    ("C", "E", 50),
    ("D", "E", 10),
    ("D", "Destination", 60),
    ("E", "Destination", 80)
]

G.add_weighted_edges_from(edges)

# Sidebar
st.sidebar.header("Options")
show_graph = st.sidebar.checkbox("Show Graph", value=True)

# Compute shortest path from Origin to Destination
shortest_path = nx.dijkstra_path(G, source="Origin", target="Destination", weight="weight")
path_length = nx.dijkstra_path_length(G, source="Origin", target="Destination", weight="weight")

st.subheader("🚦 Shortest Path from Origin to Destination")
st.write(" ➡️  ", " → ".join(shortest_path))
st.success(f"Total Distance: {path_length} miles")

# Visualize the graph
if show_graph:
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, font_size=12)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    path_edges = list(zip(shortest_path, shortest_path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=3)
    st.pyplot(plt)

# Additional options
if st.sidebar.checkbox("Show All Distances Table"):
    st.subheader("📋 Mileage Table Between Towns")
    st.dataframe({
        'From': [e[0] for e in edges],
        'To': [e[1] for e in edges],
        'Distance (miles)': [e[2] for e in edges]
    })
