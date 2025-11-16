import streamlit as st
import pandas as pd
from component.database import Database

db = Database(
    uri=st.secrets["URI"]
    ,username=st.secrets["USERNAME"]
    ,password=st.secrets["PASSWORD"]
)

st.set_page_config(page_title="Influential Commenter Analysis")

st.markdown("# Influential Commenter Analysis")

st.markdown("### Reach of High Reputation User")
st.info("Reach = Count of users who have commented on the same recipes as the top N highest-reputation users")

col1, col2 = st.columns([2,4])

with col1:
    n = st.number_input(
        'Select number of users (N)',
        min_value = 3,
        value = 10,
        step = 1
    )

df = db.run_cypher(
    query=db.generate_query(
        cypher_filename='get_high_rep_user_comment_reach.cypher'
    ).format(
        n=n
    )
    ,database=st.secrets["DATABASE"]
)

df_display = pd.DataFrame({
    'User': df['top_users.user_name'],
    'Reputation': df['top_users.user_reputation'],
    'Reach': df['reach'],
})
df_display.index = range(1, len(df_display) + 1)

st.dataframe(df_display)
