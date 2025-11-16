import streamlit as st
from component.database import Database

db = Database(
    uri=st.secrets["URI"]
    ,username=st.secrets["USERNAME"]
    ,password=st.secrets["PASSWORD"]
)

st.title("Recipe Reviews & User Feedback Analysis")

st.write(db.run_cypher(
    query=db.generate_query(
        cypher_filename='get_high_rep_user_comment_reach.cypher'
    )
    ,database=st.secrets["DATABASE"]
))

