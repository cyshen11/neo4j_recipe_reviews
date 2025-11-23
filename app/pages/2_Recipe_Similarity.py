"""
This script creates a Streamlit web page to explore recipe similarity based on
shared commenters. The data is sourced from a Neo4j graph database.

The page allows a user to select a recipe and view a ranked list of other recipes
that have been commented on by the same users. It also provides an interactive
graph visualization showing the selected similar recipe and the commenters they share
with the original recipe.
"""

import streamlit as st
import pandas as pd
from component.database import Database
import networkx as nx
from streamlit_agraph import agraph, Node, Edge, Config

# Initialize a connection to the Neo4j database using credentials from Streamlit secrets.
db = Database(
    uri=st.secrets["URI"],
    username=st.secrets["USERNAME"],
    password=st.secrets["PASSWORD"],
)

st.set_page_config(page_title="Recipe Similarity", layout="wide")

st.markdown("# Recipe Similarity")

st.info("What recipes are most similar to each other based on commenter overlap?")

pagecol1, pagecol2 = st.columns(2)

with pagecol1:

    # Fetch the list of all available recipes to populate the selection dropdown.
    all_recipes = db.run_cypher(
        query=db.generate_query(cypher_filename="get_all_recipes.cypher"),
        database=st.secrets["DATABASE"],
    )

    # User input to select a recipe to analyze for similarity.
    recipe = st.selectbox("Select recipe", all_recipes["recipe_name"])

    st.markdown("Most similar recipes")

    # Execute a Cypher query to find recipes similar to the selected one.
    # Similarity is determined by the number of users who commented on both recipes.
    similar_recipes = db.run_cypher(
        query=db.generate_query(cypher_filename="get_similar_recipes.cypher").format(
            recipe=recipe
        ),
        database=st.secrets["DATABASE"],
    )

    # Prepare the DataFrame for display, showing similar recipes and the count of shared commenters.
    df = pd.DataFrame(
        {
            "Recipe": similar_recipes["recipe_name"],
            "Shared Commenter Count": similar_recipes["shared_commenter_count"],
        }
    )
    df.index = range(1, len(df) + 1)

    st.dataframe(df)


with pagecol2:

    # User input to select one of the similar recipes for graph visualization.
    similar_recipe = st.selectbox(
        "Select similar recipe to view the shared commenters",
        similar_recipes["recipe_name"],
    )

    # Filter the `similar_recipes` DataFrame to get the list of shared commenters
    # for the recipe selected for visualization.
    commenters = similar_recipes.query(f"recipe_name == '{similar_recipe}'")

    # --- 1. Create a networkx graph object ---
    # This graph will represent the selected similar recipe and the shared commenters.
    G = nx.Graph()

    # Add the selected similar recipe as a central, larger node.
    G.add_node(similar_recipe, size=25, title=similar_recipe)
    # Add nodes for each shared commenter and create an edge connecting them to the recipe node.
    for c in commenters["shared_commenters"].values[0]:
        G.add_node(c, size=5, title=c)
        G.add_edge(c, similar_recipe)

    # --- 2. Convert networkx graph to a list of Nodes and Edges ---
    # The `streamlit-agraph` component requires nodes and edges to be in a specific format.
    nodes = [
        Node(
            id=n,
            label=str(n),
            size=G.nodes[n].get(
                "size", 10
            ),  # Use size defined in networkx, default to 10.
        )
        for n in G.nodes
    ]

    edges = [
        Edge(
            source=v, target=u, label=""  # Edges are not labeled in this visualization.
        )
        for u, v in G.edges
    ]

    # --- 3. Configure the graph's appearance ---
    # These settings control the layout and physics of the interactive graph.
    config = Config(
        width=400, height=300, directed=True, physics=True, hierarchical=False
    )

    # Render the interactive graph in the Streamlit app.
    return_value = agraph(nodes=nodes, edges=edges, config=config)
