import streamlit as st
import pandas as pd
from component.database import Database

db = Database(
    uri=st.secrets["URI"]
    ,username=st.secrets["USERNAME"]
    ,password=st.secrets["PASSWORD"]
)

st.markdown("# Recipe Journey")

st.info("""
Commenting journey of a new user. 

What are the first 3 recipes they comment on?
""")

df = db.run_cypher(
    query=db.generate_query(
        cypher_filename='get_new_user_commenting_journey.cypher'
    )
    ,database=st.secrets["DATABASE"]
)

st.dataframe(
    pd.DataFrame({
        'Commenting Path': df['commenting_path'].apply(lambda x: '  →  '.join(x)),
        'User Count': df['user_count']
    }), 
    hide_index=True
)
