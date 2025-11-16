import streamlit as st
from component.database import Database
import pandas as pd

db = Database(
    uri=st.secrets["URI"]
    ,username=st.secrets["USERNAME"]
    ,password=st.secrets["PASSWORD"]
)

st.title("Recipe Reviews & User Feedback Analysis")

tab1, tab2, tab3 = st.tabs(["Influential Commenter Analysis", "", ""])

with tab1:
    st.header("Reach of Top N Highest Reputation Users")
    st.info("Reach = Count of users who have commented on the same recipes")

    col1, col2 = st.columns([2,4])

    with col1:
        n = st.number_input(
            'Select number of users',
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

