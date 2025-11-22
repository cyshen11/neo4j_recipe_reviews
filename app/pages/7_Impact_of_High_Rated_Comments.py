import streamlit as st
import pandas as pd
from component.database import Database

db = Database(
    uri=st.secrets["URI"]
    ,username=st.secrets["USERNAME"]
    ,password=st.secrets["PASSWORD"]
)

st.markdown("# Impact of High-Rated Comments")

st.info("""
How does a 5-star comment from a high-reputation user affect subsequent commenting activity on a recipe? 

For a given recipe, what is the total reply_count and thumbs_up on comments posted after a 5-star comment from a high-reputation user?

*High reputation users = top 100 users with the highest reputation*
""")

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

df = db.run_cypher(
    query=db.generate_query(
        cypher_filename='get_reply_count_thumbs_up.cypher'
    ).format(
        recipe=recipe
    )
    ,database=st.secrets["DATABASE"]
)
# convert unix timestamp (seconds or milliseconds) to datetime
if df['created_at'].max() > 1e12:
    df['created_at'] = pd.to_datetime(df['created_at'], unit='ms', errors='coerce')
else:
    df['created_at'] = pd.to_datetime(df['created_at'], unit='s', errors='coerce')

if df.shape[0] >= 1:
    st.markdown("First 5-star comment")
    st.dataframe(
        pd.DataFrame({
            'User': df['user'],
            'Reputation': df['user_reputation'],
            'Posted': df['created_at'],
            'Comment': df['comment']
        }),
        hide_index=True
    )

    col1, col2, col3 = st.columns([1, 1, 3])
    col1.metric('Total Reply Count', df['total_reply_count'][0])
    col2.metric('Total Thumbs-Up', df['total_thumbs_up'][0])
