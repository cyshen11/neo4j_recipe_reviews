"""
This script creates a Streamlit web page to analyze the "chain of influence"
for individual users from a recipe review dataset stored in a Neo4j database.

The page allows for the selection of a user (from a list sorted by reputation)
and displays key metrics about their influence. This includes their reputation score
and the average number of "thumbs-up" their comments have received. It also
provides a detailed table of all comments made by that user, including the comment
text, thumbs-up count, creation date, and the associated recipe.
"""

import streamlit as st
import pandas as pd
from component.database import Database
import numpy as np

# Initialize a connection to the Neo4j database using credentials from Streamlit secrets.
db = Database(
    uri=st.secrets["URI"],
    username=st.secrets["USERNAME"],
    password=st.secrets["PASSWORD"],
)

st.markdown("# Chain of Influence")

# Provide a description of the analysis for the user.
st.info(
    """
Trace the user_reputation or thumbs_up scores through the network. 

For a specific high-reputation user, what is the average thumbs_up count of the comments on the recipes they have also commented on? 

This measures their indirect influence on a recipe's overall engagement.
"""
)

# Fetch a list of all users, sorted by their reputation score, to populate the dropdown.
user_sort_by_rep = db.run_cypher(
    query=db.generate_query(cypher_filename="get_users_sort_by_rep.cypher"),
    database=st.secrets["DATABASE"],
)

# User input to select a user to analyze.
user = st.selectbox("Select user", user_sort_by_rep["user_name"])
# Retrieve the reputation score for the selected user from the DataFrame.
reputation = user_sort_by_rep.query(f"user_name == '{user}'")["user_reputation"].values[
    0
]

col1, col2, col3 = st.columns([1, 2, 2])

# Display the selected user's reputation in a metric card.
col1.metric(label="Reputation", value=reputation)

comments = db.run_cypher(
    query=db.generate_query(cypher_filename="get_comments.cypher").format(user=user),
    database=st.secrets["DATABASE"],
)
# Convert the 'created_at' Unix timestamp to a readable datetime format.
# The logic checks if the timestamp is likely in milliseconds ( > 1e12) or seconds
# and converts it accordingly. This handles potential inconsistencies in the source data.
if comments["created_at"].max() > 1e12:
    comments["created_at"] = pd.to_datetime(
        comments["created_at"], unit="ms", errors="coerce"
    )
else:
    comments["created_at"] = pd.to_datetime(
        comments["created_at"], unit="s", errors="coerce"
    )

# Calculate and display the average thumbs-up count for the user's comments.
col2.metric(label="Average Thumbs-up Count", value=int(np.mean(comments["thumbs_up"])))

# Display a detailed table of the user's comments.
st.dataframe(
    pd.DataFrame(
        {
            "Comment": comments["comment"],
            "Thumbs-up": comments["thumbs_up"],
            "Posted": comments["created_at"],
            "Recipe": comments["recipe"],
        }
    ),
    hide_index=True,
)  # Hide the default DataFrame index for a cleaner presentation.
