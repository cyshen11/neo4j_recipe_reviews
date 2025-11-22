import streamlit as st
import pandas as pd
from component.database import Database
import numpy as np

db = Database(
    uri=st.secrets["URI"]
    ,username=st.secrets["USERNAME"]
    ,password=st.secrets["PASSWORD"]
)

st.markdown("# Chain of Influence")

st.info("""
Trace the user_reputation or thumbs_up scores through the network. 

For a specific high-reputation user, what is the average thumbs_up count of the comments on the recipes they have also commented on? 

This measures their indirect influence on a recipe's overall engagement.
""")

user_sort_by_rep = db.run_cypher(
    query=db.generate_query(
        cypher_filename='get_users_sort_by_rep.cypher'
    )
    ,database=st.secrets["DATABASE"]
)

user = st.selectbox(
    'Select user',
    user_sort_by_rep['user_name']
)
reputation = user_sort_by_rep.query(f"user_name == '{user}'")['user_reputation'].values[0]

col1, col2, col3 = st.columns([1, 2, 2])

col1.metric(label="Reputation", value=reputation)

comments = db.run_cypher(
    query=db.generate_query(
        cypher_filename='get_comments.cypher'
    ).format(
        user=user
    )
    ,database=st.secrets["DATABASE"]
)
# convert unix timestamp (seconds or milliseconds) to datetime
if comments['created_at'].max() > 1e12:
    comments['created_at'] = pd.to_datetime(comments['created_at'], unit='ms', errors='coerce')
else:
    comments['created_at'] = pd.to_datetime(comments['created_at'], unit='s', errors='coerce')

col2.metric(label="Average Thumbs-up Count", value=int(np.mean(comments['thumbs_up'])))

st.dataframe(comments, hide_index=True)

