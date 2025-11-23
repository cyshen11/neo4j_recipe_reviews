import streamlit as st

st.set_page_config(
    page_title="Homepage"
)

st.title("Recipe Reviews & User Feedback Analysis")
st.sidebar.success("Select a page above.")

st.markdown("""
This app demonstrates different analyses that can be performed on the [Recipe Reviews and User Feedback](https://archive.ics.uci.edu/dataset/911/recipe+reviews+and+user+feedback+dataset) dataset from the UCI Machine Learning Repository.

The dataset is ingested into a Neo4j graph database, and the analyses are performed using Cypher queries.
""")