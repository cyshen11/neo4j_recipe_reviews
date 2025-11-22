import streamlit as st
import pandas as pd
from component.database import Database

db = Database(
    uri=st.secrets["URI"]
    ,username=st.secrets["USERNAME"]
    ,password=st.secrets["PASSWORD"]
)

st.markdown("# Outlier Detection")

st.info("""
Identify users who comment on a diverse range of recipes that have little to no commenter overlap with one another. 

This could point to users with eclectic tastes or those who are not part of any specific community.
""")

df = db.run_cypher(
    query=db.generate_query(
        cypher_filename='get_outlier_users.cypher'
    )
    ,database=st.secrets["DATABASE"]
)

st.dataframe(df)