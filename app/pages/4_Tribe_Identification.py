import streamlit as st
import pandas as pd
from component.database import Database
import networkx as nx
from pyvis.network import Network
from streamlit_agraph import agraph, Node, Edge, Config
import colorsys

db = Database(
    uri=st.secrets["URI"]
    ,username=st.secrets["USERNAME"]
    ,password=st.secrets["PASSWORD"]
)

st.markdown("# Tribe Identification")

st.info("""
Clusters of users who have commented on same recipes. This could be used to identify communities or "tribes" of users with shared interests, even if they don't directly interact.

If there is error, click *Create tribes*. *Query tribes* only get first 5 users for each tribe.
""")

if st.button("Create tribes"):
    db.run_cypher(
        query=db.generate_query(
            cypher_filename='create_tribe_graph.cypher'
        )
        ,database=st.secrets["DATABASE"]
    )

col1, col2 = st.columns([4, 1]) 

with col1:
    df = db.run_cypher(
        query=db.generate_query(
            cypher_filename='get_tribes.cypher'
        )
        ,database=st.secrets["DATABASE"]
    )

    # determine which column holds the user id/name
    user_col = 'user' if 'user' in df.columns else ('user_name' if 'user_name' in df.columns else df.columns[0])

    recipes = df['recipe'].dropna().unique().tolist()

    # map each user to their community (take first if multiple rows per user)
    user_communities = df.dropna(subset=[user_col]).groupby(user_col)['communityId'].first().to_dict()

    # build palette for communities
    unique_communities = [c for c in sorted(df['communityId'].dropna().unique().tolist())]
    def _hsl_to_hex(h):
        r, g, b = colorsys.hls_to_rgb(h, 0.5, 0.65)
        return '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
    community_colors = {c: _hsl_to_hex(i / max(len(unique_communities), 1)) for i, c in enumerate(unique_communities)}
    default_recipe_color = '#CCCCCC'
    default_user_color = '#888888'

    # --- 1. Create a networkx graph ---
    G = nx.Graph()

    # add recipe nodes (neutral color)
    for r in recipes:
        G.add_node(r, size=25, title=r, color=default_recipe_color)

    # add user nodes colored by community
    users = list(user_communities.keys())
    for u in users:
        comm = user_communities.get(u)
        color = community_colors.get(comm, default_user_color)
        G.add_node(u, size=5, title=str(comm), color=color)

    # add edges (one edge per user-recipe row)
    for _, row in df.iterrows():
        u = row.get(user_col)
        rec = row.get('recipe')
        if pd.isna(u) or pd.isna(rec):
            continue
        G.add_edge(u, rec)

    # --- 2. Convert networkx graph to a list of Nodes and Edges ---
    nodes = [Node(
        id=n,
        label=str(n),
        size=G.nodes[n].get('size', 10),
        title=G.nodes[n].get('title', ''),
        color=G.nodes[n].get('color', '')
    ) for n in G.nodes]

    edges = [Edge(
        source=u,
        target=v,
        label='',
        weight=G.edges[u,v].get('weight', 2)
    ) for u, v in G.edges]

    # --- 3. Configure the graph's appearance ---
    config = Config(
        width=800,
        height=400,
        directed=False,
        physics=True,
        hierarchical=False
    )

    return_value = agraph(
        nodes=nodes,
        edges=edges,
        config=config
    )

with col2:
    bridge_users = db.run_cypher(
        query=db.generate_query(
            cypher_filename='get_bridge_users.cypher'
        )
        ,database=st.secrets["DATABASE"]
    )

    st.dataframe(pd.DataFrame({'"Bridge" User': bridge_users['user_name']}), hide_index=True)