import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from PIL import Image

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

# Define the graph with renamed towns
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

# Cost and time info per commute method
commute_methods = {
    "Drive": {"cost_per_mile": 0.5, "time_per_mile": 1.2},
    "Bike": {"cost_per_mile": 0.1, "time_per_mile": 4},
    "Taxi": {"cost_per_mile": 2.0, "time_per_mile": 1.0}
}

# Form layout (not sidebar)
st.header("Route Control Panel")

col1, col2 = st.columns(2)
with col1:
    show_graph = st.checkbox("Show Town Network Graph", True)
with col2:
    show_table = st.checkbox("Show Road Distance Table", False)

st.markdown("---")
start = st.selectbox("Select Start Town", list(towns.values()), index=0)
end = st.selectbox("Select End Town", list(towns.values()), index=len(towns)-1)
commute = st.radio("Choose Commute Method", list(commute_methods.keys()))

if st.button("Find Route"):
    try:
        route = nx.dijkstra_path(G, source=start, target=end, weight="weight")
        distance = nx.dijkstra_path_length(G, source=start, target=end, weight="weight")

        st.subheader(f"🗺️ Route from {start} to {end} via {commute}")
        st.markdown(" → ".join(route))

        # Calculate cost and time
        cost_per_mile = commute_methods[commute]["cost_per_mile"]
        time_per_mile = commute_methods[commute]["time_per_mile"]
        total_cost = distance * cost_per_mile
        total_time = distance * time_per_mile

        st.success(f"Total Distance: {distance} miles")
        st.info(f"Estimated Cost: ${total_cost:.2f}")
        st.info(f"Estimated Time: {total_time:.1f} minutes")

        # Route-specific image (simulated roadside views)
        images = {
            ("Chicago", "Bayview"): "https://upload.wikimedia.org/wikipedia/commons/9/9a/Route66Road.jpg",
            ("Chicago", "Mclain"): "https://upload.wikimedia.org/wikipedia/commons/0/0c/Rural_road_in_Illinois.jpg",
            ("Aurora", "Bayview"): "https://upload.wikimedia.org/wikipedia/commons/f/f2/Scenic_road_trip.jpg",
            ("Smallville", "Bayview"): "https://upload.wikimedia.org/wikipedia/commons/7/75/Countryside_Road.jpg"
        }

        for key, img_url in images.items():
            if key[0] in route and key[1] in route:
                st.image(img_url, caption="Scenic Roadside View", use_column_width=True)
                break

        # Show graph
        if show_graph:
            pos = nx.spring_layout(G, seed=42)
            edge_labels = nx.get_edge_attributes(G, 'weight')
            plt.figure(figsize=(10, 6))
            nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, font_size=12)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            route_edges = list(zip(route, route[1:]))
            nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color='red', width=3)
            st.pyplot(plt)

    except nx.NetworkXNoPath:
        st.error("No path found between the selected towns.")

# Show road distance table
if show_table:
    st.subheader("📋 Road Distances Table")
    st.dataframe({
        'From': [e[0] for e in edges],
        'To': [e[1] for e in edges],
        'Distance (miles)': [e[2] for e in edges]
    })
