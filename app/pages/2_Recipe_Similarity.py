import streamlit as st
import pandas as pd
from component.database import Database
import networkx as nx
from pyvis.network import Network
from streamlit_agraph import agraph, Node, Edge, Config

db = Database(
    uri=st.secrets["URI"]
    ,username=st.secrets["USERNAME"]
    ,password=st.secrets["PASSWORD"]
)

st.set_page_config(page_title="Recipe Similarity", layout="wide")

st.markdown("# Recipe Similarity")

st.markdown("What recipes are most similar to each other based on commenter overlap?")

pagecol1, pagecol2 = st.columns(2)

with pagecol1:

    all_recipes = db.run_cypher(
        query=db.generate_query(
            cypher_filename='get_all_recipes.cypher'
        )
        ,database=st.secrets["DATABASE"]
    )

    recipe = st.selectbox(
        'Select recipe',
        all_recipes['recipe_name']
    )

    st.markdown("Most similar recipes")

    similar_recipes = db.run_cypher(
        query=db.generate_query(
            cypher_filename='get_similar_recipes.cypher'
        ).format(
            recipe=recipe
        )
        ,database=st.secrets["DATABASE"]
    )

    df = pd.DataFrame({
        'Recipe': similar_recipes['recipe_name'],
        'Shared Commenter Count': similar_recipes['shared_commenter_count']
    })
    df.index = range(1, len(df) + 1)

    st.dataframe(df)


with pagecol2:

    similar_recipe = st.selectbox(
        'Select similar recipe to view the shared commenters',
        similar_recipes['recipe_name']
    )

    commenters = similar_recipes.query(f"recipe_name == '{similar_recipe}'")

    # --- 1. Create a networkx graph ---
    G = nx.Graph()

    G.add_node(similar_recipe, size=25, title=similar_recipe)
    for c in commenters['shared_commenters'].values[0]:
        G.add_node(c, size = 5, title=c)
        G.add_edge(c, similar_recipe)

    # --- 2. Convert networkx graph to a list of Nodes and Edges ---
    nodes = [Node(
        id=n,
        label=str(n),
        size=G.nodes[n].get('size', 10),
        title=G.nodes[n].get('title', '')
    ) for n in G.nodes]

    edges = [Edge(
        source=v,
        target=u,
        label=''
    ) for u, v in G.edges]

    # --- 3. Configure the graph's appearance ---
    config = Config(
        width=400,
        height=300,
        directed=True,
        physics=True,
        hierarchical=False
    )

    return_value = agraph(
        nodes=nodes,
        edges=edges,
        config=config
    )
