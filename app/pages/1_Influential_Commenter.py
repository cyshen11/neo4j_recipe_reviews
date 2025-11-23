"""
This script creates a Streamlit web page to analyze and visualize the influence
of high-reputation users within a recipe review dataset stored in a Neo4j graph database.

The page allows users to identify the top N most reputable users and explore their "reach,"
defined as the number of other users who have commented on the same recipes. It also provides
an interactive graph visualization of these connections for a selected user."""
import streamlit as st
import pandas as pd
from component.database import Database
import networkx as nx
from pyvis.network import Network
from streamlit_agraph import agraph, Node, Edge, Config

# Initialize a connection to the Neo4j database using credentials from Streamlit secrets.
db = Database(
    uri=st.secrets["URI"]
    ,username=st.secrets["USERNAME"]
    ,password=st.secrets["PASSWORD"]
)

st.set_page_config(page_title="Influential Commenter", layout="wide")

st.markdown("# Influential Commenter")

st.markdown("### Reach of High Reputation User")
st.info("""
What is the reach of a high-reputation user's comments?

Reach = Count of users who have commented on the same recipes as the top N highest-reputation users
""")

pagecol1, pagecol2 = st.columns(2)

with pagecol1:

    col1, col2 = st.columns(2)

    with col1:
        # User input to select the number of top users (N) to analyze.
        n = st.number_input(
            'Select number of users (N)',
            min_value = 3,
            value = 10,
            step = 1
        )

    # Execute a Cypher query to get the top N users by reputation and their comment reach.
    # The query is loaded from a file and formatted with the user-selected value of N.
    df = db.run_cypher(
        query=db.generate_query(
            cypher_filename='get_high_rep_user_comment_reach.cypher'
        ).format(
            n=n
        )
        ,database=st.secrets["DATABASE"]
    )

    # Prepare the DataFrame for display by selecting and renaming columns.
    df_display = pd.DataFrame({
        'User': df['top_users.user_name'],
        'Reputation': df['top_users.user_reputation'],
        'Reach': df['reach'],
    })
    df_display.index = range(1, len(df_display) + 1)

    st.dataframe(df_display)

with pagecol2:

    # --- Visualization --- #
    col3, col4 = st.columns(2)
    with col3:
        user = st.selectbox("Select user to view user's reach", df['top_users.user_name'])
    # User input to filter connections by a minimum number of shared recipes.
    with col4:
        recipe_count = st.number_input(
            # This helps in reducing noise in the graph visualization.
            'Select min. # recipe count',
            min_value = 2,
            value = 2,
            step = 1
        )
    df_reached_user = db.run_cypher(
        query=db.generate_query(
            # This query finds all users who have commented on at least `recipe_count`
            # same recipes as the selected `user`.
            cypher_filename='get_reached_user.cypher'
        ).format(
            user=user,
            recipe_count=recipe_count
        )
        ,database=st.secrets["DATABASE"]
    )
    # Display an informational message with the average reputation of the reached users.
    st.info(f"""Filtered to users have commented on at least {recipe_count} same recipes. **Average reputation of users: {round(df_reached_user['reached_user_reputation'].mean())}**""")

    # --- 1. Create a networkx graph object ---
    # This graph will represent the selected user and the other users they have reached.
    G = nx.Graph()

    # Add the selected influential user as a central, larger node.
    G.add_node(user, size=25, title=user)
    # Add nodes for each "reached" user and edges connecting them to the central user.
    for u, recipe_count in zip(df_reached_user['reached_user'].values, df_reached_user['recipe_count'].values):
        G.add_node(u, size = 5, title=u)
        # The edge weight represents the number of shared recipes.
        G.add_edge(user, u, weight=int(recipe_count), label="Reach")

    # --- 2. Convert networkx graph to a list of Nodes and Edges ---
    # The `streamlit-agraph` component requires nodes and edges to be in a specific format.
    nodes = [Node(
        id=n,
        label=str(n),
        size=G.nodes[n].get('size', 10) # Use size defined in networkx, default to 10.
    ) for n in G.nodes]

    edges = [Edge(
        source=u,
        target=v,
        label='',
        weight=G.edges[u,v].get('weight', 2)
    ) for u, v in G.edges]

    # --- 3. Configure the graph's appearance ---
    # These settings control the layout and physics of the interactive graph.
    config = Config(
        width=400,
        height=300,
        directed=True,
        physics=True,
        hierarchical=False
    )

    # Render the interactive graph in the Streamlit app.
    return_value = agraph(
        nodes=nodes,
        edges=edges,
        config=config
    )
