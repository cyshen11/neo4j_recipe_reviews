"""
This script creates a Streamlit web page to analyze the initial "commenting journey"
of new users within a recipe review dataset from a Neo4j database.

The analysis identifies the first three recipes that new users comment on, treating
this sequence as their initial "journey." The script aggregates these journeys
across all new users to find the most common paths. The results are displayed in a
table, showing each unique journey and the number of users who followed that path.
This can provide insights into user onboarding and initial engagement patterns.
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

st.markdown("# Recipe Journey")

# Provide a description of the analysis for the user.
st.info("""
Commenting journey of a new user. What are the first 3 recipes they comment on?
""")

# Execute a Cypher query to get the initial commenting journeys for new users.
# The query logic is contained in the specified .cypher file.
df = db.run_cypher(
    query=db.generate_query(
        cypher_filename='get_new_user_commenting_journey.cypher'
    )
    ,database=st.secrets["DATABASE"]
)

# Display the results in a Streamlit DataFrame.
st.dataframe(
    pd.DataFrame({
        # The 'commenting_path' column from the query is a list of recipe names.
        # This lambda function formats the list into a more readable string.
        'Commenting Journey': df['commenting_path'].apply(lambda x: ' → '.join(x)),
        'User Count': df['user_count']
    }), 
    # Hide the default DataFrame index for a cleaner presentation.
    hide_index=True
)
