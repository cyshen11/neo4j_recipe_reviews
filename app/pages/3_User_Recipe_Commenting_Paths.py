"""
This script creates a Streamlit web page to analyze user commenting behavior
by identifying common "commenting paths" from a selected recipe. The data is
sourced from a Neo4j graph database.

A "commenting path" is a sequence of recipes that a user comments on after
commenting on an initial, user-selected recipe. This analysis helps uncover
patterns in user interests and how they navigate between different recipes.
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

st.markdown("# User-Recipe Commenting Paths")

# Provide a description of the analysis for the user.
st.info("""What are the most common paths a user takes when commenting on recipes? 

For example, do users who comment on baking recipes tend to also comment on a specific type of dessert recipe? 
This uncovers user behavior patterns.""")

all_recipes = db.run_cypher(
    query=db.generate_query(
        # Fetch the list of all available recipes to populate the selection dropdown.
        cypher_filename='get_all_recipes.cypher'
    )
    ,database=st.secrets["DATABASE"]
)

# User input to select a starting recipe for the path analysis.
recipe = st.selectbox(
    'Select recipe',
    all_recipes['recipe_name']
)

# Execute a Cypher query to find the commenting paths starting from the selected recipe.
commenting_paths = db.run_cypher(
    query=db.generate_query(
        # This query identifies sequences of recipes commented on by the same users
        # after they have commented on the initial selected recipe.
        cypher_filename='get_user_commenting_paths.cypher'
    ).replace('{recipe}', recipe)
    ,database=st.secrets["DATABASE"]
)

# Display the results in a Streamlit DataFrame.
st.dataframe(
    pd.DataFrame({
        # The 'commenting_path' column from the query result is a list of recipe names.
        # This lambda function formats the list into a more readable string format.
        'Commenting Path': commenting_paths['commenting_path'].apply(lambda x: ' → '.join(x)),
        'User Count': commenting_paths['user_count']
    }), 
    # Hide the default DataFrame index for a cleaner presentation.
    hide_index=True
)
