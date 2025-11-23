"""
This script creates a Streamlit web page for identifying and visualizing user
"tribes" or communities within a recipe review dataset from a Neo4j database.

The analysis relies on community detection algorithms (e.g., Louvain) run directly
on the Neo4j graph. The page allows a user to trigger the community detection
process and then visualizes the results as an interactive graph. In the graph,
users are colored by their community ID, showing clusters of users who comment on
similar recipes. The page also identifies and lists "bridge" users, who are
instrumental in connecting different communities.
"""

import streamlit as st
import pandas as pd
from component.database import Database
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config
import colorsys

# Initialize a connection to the Neo4j database using credentials from Streamlit secrets.
db = Database(
    uri=st.secrets["NEO4J_URI"],
    username=st.secrets["NEO4J_USERNAME"],
    password=st.secrets["NEO4J_PASSWORD"],
)

st.markdown("# Tribe Identification")

st.info(
    """
Clusters of users who have commented on same recipes. This could be used to identify communities or "tribes" of users with shared interests, even if they don't directly interact.

If there is an error, click `Create tribes` button below. `Query tribes` will only get first 5 users for each tribe.
"""
)

# This button executes a Cypher query that runs a community detection algorithm
# (like Louvain) in Neo4j and saves the community ID for each user.
# This can be a long-running operation.
if st.button("Create tribes"):
    db.run_cypher(
        query=db.generate_query(cypher_filename="create_tribe_graph.cypher"),
        database=st.secrets["NEO4J_DATABASE"],
    )

col1, col2 = st.columns([4, 1])

with col1:
    # Fetch the community data, which includes users, their assigned community IDs,
    # and the recipes they've commented on.
    df = db.run_cypher(
        query=db.generate_query(cypher_filename="get_tribes.cypher"),
        database=st.secrets["NEO4J_DATABASE"],
    )

    # Robustly determine which column in the DataFrame holds the user identifier.
    user_col = (
        "user"
        if "user" in df.columns
        else ("user_name" if "user_name" in df.columns else df.columns[0])
    )

    # Get a unique list of all recipes involved in the communities.
    recipes = df["recipe"].dropna().unique().tolist()

    # Create a dictionary mapping each user to their assigned community ID.
    # `first()` is used in case a user appears in multiple rows.
    user_communities = (
        df.dropna(subset=[user_col]).groupby(user_col)["communityId"].first().to_dict()
    )

    # --- Color Palette Generation for Communities ---
    # Get a sorted list of unique community IDs to ensure consistent color mapping.
    unique_communities = [
        c for c in sorted(df["communityId"].dropna().unique().tolist())
    ]

    # Helper function to convert HSL color values to a hex string for HTML/CSS.
    def _hsl_to_hex(h):
        r, g, b = colorsys.hls_to_rgb(h, 0.5, 0.65)
        return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

    # Generate a distinct color for each community by evenly spacing hues in the HSL color space.
    community_colors = {
        c: _hsl_to_hex(i / max(len(unique_communities), 1))
        for i, c in enumerate(unique_communities)
    }
    default_recipe_color = "#CCCCCC"
    default_user_color = "#888888"

    # --- 1. Create a networkx graph object ---
    G = nx.Graph()

    # Add recipe nodes to the graph with a default neutral color.
    for r in recipes:
        G.add_node(r, size=25, title=r, color=default_recipe_color)

    # Add user nodes to the graph, coloring each node based on its community ID.
    users = list(user_communities.keys())
    for u in users:
        comm = user_communities.get(u)
        color = community_colors.get(comm, default_user_color)
        G.add_node(u, size=5, title=str(comm), color=color)

    # Add edges between users and the recipes they have commented on.
    for _, row in df.iterrows():
        u = row.get(user_col)
        rec = row.get("recipe")
        if pd.isna(u) or pd.isna(rec):
            continue
        G.add_edge(u, rec)

    # --- 2. Convert networkx graph to a list of Nodes and Edges ---
    # The `streamlit-agraph` component requires nodes and edges to be in a specific format.
    nodes = [
        Node(
            id=n,
            label=str(n),
            size=G.nodes[n].get("size", 10),
            title=G.nodes[n].get("title", ""),
            color=G.nodes[n].get("color", ""),
        )
        for n in G.nodes
    ]

    edges = [
        Edge(
            source=u, target=v, label=""  # Edges are not labeled in this visualization.
        )
        for u, v in G.edges
    ]

    # --- 3. Configure the graph's appearance ---
    # These settings control the layout and physics of the interactive graph.
    config = Config(
        width=800, height=400, directed=False, physics=True, hierarchical=False
    )

    # Render the interactive graph in the Streamlit app.
    return_value = agraph(nodes=nodes, edges=edges, config=config)

with col2:
    # In a separate column, display "bridge" users. These are users who connect
    # different communities, identified by a separate Cypher query.
    bridge_users = db.run_cypher(
        query=db.generate_query(cypher_filename="get_bridge_users.cypher"),
        database=st.secrets["NEO4J_DATABASE"],
    )

    st.dataframe(
        pd.DataFrame({'"Bridge" User': bridge_users["user_name"]}), hide_index=True
    )
