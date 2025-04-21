import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# App title
st.title("🚗 Interactive Route Optimizer Between Towns")

# Town name mappings
towns = {
    "Origin": "Chicago",
    "A": "Mclain",
    "B": "Aurora",
    "C": "Paker",
    "D": "Smallville",
    "E": "Farmer",
    "Destination": "Bayview"
}

# Define graph
G = nx.Graph()
edges = [
    ("Chicago", "Mclain", 40),
    ("Chicago", "Aurora", 60),
    ("Chicago", "Paker", 50),
    ("Mclain", "Aurora", 10),
    ("Mclain", "Smallville", 70),
    ("Aurora", "Paker", 20),
    ("Aurora", "Smallville", 55),
    ("Aurora", "Farmer", 40),
    ("Paker", "Farmer", 50),
    ("Smallville", "Farmer", 10),
    ("Smallville", "Bayview", 60),
    ("Farmer", "Bayview", 80)
]
G.add_weighted_edges_from(edges)

# Sidebar
st.sidebar.header("Options")
show_graph = st.sidebar.checkbox("Show Town Network", True)
show_table = st.sidebar.checkbox("Show Road Distances", False)
show_faq = st.sidebar.checkbox("Answer Questions", True)

# Compute shortest path
shortest_path = nx.dijkstra_path(G, source="Chicago", target="Bayview", weight="weight")
path_length = nx.dijkstra_path_length(G, source="Chicago", target="Bayview", weight="weight")

st.subheader("🚦 Shortest Path from Chicago to Bayview")
st.write(" → ".join(shortest_path))
st.success(f"Total Distance: {path_length} miles")

# Show graph
if show_graph:
    pos = nx.spring_layout(G, seed=42)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    plt.figure(figsize=(10, 6))
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=1600, font_size=11)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    path_edges = list(zip(shortest_path, shortest_path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=3)
    st.pyplot(plt)

# Show mileage table
if show_table:
    st.subheader("📋 Road Distances Table")
    st.dataframe({
        'From': [e[0] for e in edges],
        'To': [e[1] for e in edges],
        'Distance (miles)': [e[2] for e in edges]
    })

# FAQ / Problem Solution Sections
if show_faq:
    st.subheader("❓ Problem Interpretation & Questions")
    
    st.markdown("**(a) Problem as a Network**")
    st.markdown("- Nodes represent towns.")
    st.markdown("- Links represent roads (edges).")
    st.markdown("- Weights are distances (miles). See the network above.")
    
    st.markdown("**(b) Solved with Dijkstra's Algorithm**")
    st.markdown("→ Path: `" + " → ".join(shortest_path) + "`")
    st.markdown(f"→ Distance: **{path_length} miles** (via Dijkstra in `networkx`)")

    st.markdown("**(c) Spreadsheet Model**")
    st.markdown("- You can model this with Excel using a matrix of distances and apply Excel Solver to minimize total distance.")
    
    st.markdown("**(d) If distances are costs in dollars...**")
    st.markdown("- The shortest path also minimizes cost, since it uses the same weights.")
    
    st.markdown("**(e) If distances are times in minutes...**")
    st.markdown("- Yes, this would still find the minimum-time route assuming no speed change.")

# Bonus feature: user-defined start & end
st.sidebar.markdown("---")
st.sidebar.subheader("Custom Path Finder")
start = st.sidebar.selectbox("Start Town", list(towns.values()))
end = st.sidebar.selectbox("End Town", list(towns.values()))
if st.sidebar.button("Find Custom Route"):
    try:
        custom_path = nx.dijkstra_path(G, source=start, target=end, weight="weight")
        custom_dist = nx.dijkstra_path_length(G, source=start, target=end, weight="weight")
        st.markdown(f"**Shortest route from {start} to {end}:**")
        st.markdown(" → ".join(custom_path))
        st.success(f"Total Distance: {custom_dist} miles")
    except nx.NetworkXNoPath:
        st.error("No path exists between the selected towns.")
