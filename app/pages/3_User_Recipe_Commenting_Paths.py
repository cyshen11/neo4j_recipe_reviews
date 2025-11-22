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

st.markdown("# User-Recipe Commenting Paths")

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

commenting_paths = db.run_cypher(
    query=db.generate_query(
        cypher_filename='get_user_commenting_paths.cypher'
    ).replace('{recipe}', recipe)
    ,database=st.secrets["DATABASE"]
)

st.dataframe(
    pd.DataFrame({
        'Commenting Path': commenting_paths['commenting_path'].apply(lambda x: ' → '.join(x)),
        'User Count': commenting_paths['user_count']
    }), 
    hide_index=True
)
