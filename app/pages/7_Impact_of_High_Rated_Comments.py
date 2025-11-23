"""
This script creates a Streamlit web page to analyze the impact of high-rated
comments from high-reputation users on subsequent engagement with a recipe.
The data is sourced from a Neo4j graph database.

The page allows a user to select a recipe. It then identifies the first 5-star
comment posted on that recipe by a high-reputation user (defined as top 100).
After finding this pivotal comment, it calculates the total number of replies and
thumbs-up received by all comments posted *after* it. This analysis aims to
quantify the "influence" a positive, high-profile comment has on community
interaction.
"""
import streamlit as st
import pandas as pd
from component.database import Database

# Initialize a connection to the Neo4j database using credentials from Streamlit secrets.
db = Database(
    uri=st.secrets["URI"]
    ,username=st.secrets["USERNAME"]
    ,password=st.secrets["PASSWORD"]
)

st.markdown("# Impact of High-Rated Comments")

# Provide a description of the analysis for the user.
st.info("""
How does a 5-star comment from a high-reputation user affect subsequent commenting activity on a recipe? 

For a given recipe, what is the total reply_count and thumbs_up on comments posted after a 5-star comment from a high-reputation user?

*High reputation users = top 100 users with the highest reputation*
""")

# Fetch the list of all available recipes to populate the selection dropdown.
all_recipes = db.run_cypher(
    query=db.generate_query(
        cypher_filename='get_all_recipes.cypher'
    )
    ,database=st.secrets["DATABASE"]
)

# User input to select a recipe to analyze.
recipe = st.selectbox(
    'Select recipe',
    all_recipes['recipe_name']
)

# Execute a Cypher query to find the impact of the first 5-star comment from a high-rep user.
df = db.run_cypher(
    query=db.generate_query(
        # This query finds the first 5-star comment from a top-100 user on the selected recipe
        # and then aggregates the reply and thumbs-up counts of all subsequent comments.
        cypher_filename='get_reply_count_thumbs_up.cypher'
    ).format(
        recipe=recipe
    )
    ,database=st.secrets["DATABASE"]
)
# Convert the 'created_at' Unix timestamp to a readable datetime format.
# The logic checks if the timestamp is likely in milliseconds ( > 1e12) or seconds
# and converts it accordingly. This handles potential inconsistencies in the source data.
if df['created_at'].max() > 1e12:
    df['created_at'] = pd.to_datetime(df['created_at'], unit='ms', errors='coerce')
else:
    df['created_at'] = pd.to_datetime(df['created_at'], unit='s', errors='coerce')

# This block only executes if a qualifying 5-star comment was found for the selected recipe.
if df.shape[0] >= 1:
    st.markdown("First 5-star comment")
    # Display a table with details about the influential comment and the user who posted it.
    st.dataframe(
        pd.DataFrame({
            'User': df['user'],
            'Reputation': df['user_reputation'],
            'Posted': df['created_at'],
            'Comment': df['comment']
        }),
        hide_index=True # Hide the default DataFrame index for a cleaner presentation.
    )

    # Display the calculated impact metrics in separate columns.
    col1, col2, col3 = st.columns([1, 1, 3])
    col1.metric('Total Reply Count', df['total_reply_count'][0])
    col2.metric('Total Thumbs-Up', df['total_thumbs_up'][0])
