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

st.markdown("What recipes are most similar to each other based on commeter overlap?")

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

    #     n = st.number_input(
    #         'Select number of users (N)',
    #         min_value = 3,
    #         value = 10,
    #         step = 1
    #     )

    # df = db.run_cypher(
    #     query=db.generate_query(
    #         cypher_filename='get_high_rep_user_comment_reach.cypher'
    #     ).format(
    #         n=n
    #     )
    #     ,database=st.secrets["DATABASE"]
    # )

    # df_display = pd.DataFrame({
    #     'User': df['top_users.user_name'],
    #     'Reputation': df['top_users.user_reputation'],
    #     'Reach': df['reach'],
    # })
    # df_display.index = range(1, len(df_display) + 1)

    # st.dataframe(df_display)

# with pagecol2:

#     # --- Visualization --- #
#     col3, col4 = st.columns(2)
#     with col3:
#         user = st.selectbox("Select user to view user's reach", df['top_users.user_name'])
#     with col4:
#         recipe_count = st.number_input(
#             'Select min. # recipe count',
#             min_value = 2,
#             value = 2,
#             step = 1
#         )
#     df_reached_user = db.run_cypher(
#         query=db.generate_query(
#             cypher_filename='get_reached_user.cypher'
#         ).format(
#             user=user,
#             recipe_count=recipe_count
#         )
#         ,database=st.secrets["DATABASE"]
#     )
#     st.info(f"Filtered to users have commented on at least {recipe_count} same recipes")

#     # --- 1. Create a networkx graph ---
#     G = nx.Graph()

#     G.add_node(user, size=25, title=user)
#     for u, recipe_count in zip(df_reached_user['reached_user'].values, df_reached_user['recipe_count'].values):
#         G.add_node(u, size = 5, title=u)
#         G.add_edge(user, u, weight=int(recipe_count), label="Reach")

#     # --- 2. Convert networkx graph to a list of Nodes and Edges ---
#     nodes = [Node(
#         id=n,
#         label=str(n),
#         size=G.nodes[n].get('size', 10),
#         title=G.nodes[n].get('title', '')
#     ) for n in G.nodes]

#     edges = [Edge(
#         source=u,
#         target=v,
#         label='',
#         weight=G.edges[u,v].get('weight', 2)
#     ) for u, v in G.edges]

#     # --- 3. Configure the graph's appearance ---
#     config = Config(
#         width=400,
#         height=300,
#         directed=True,
#         physics=True,
#         hierarchical=False
#     )

#     return_value = agraph(
#         nodes=nodes,
#         edges=edges,
#         config=config
#     )
