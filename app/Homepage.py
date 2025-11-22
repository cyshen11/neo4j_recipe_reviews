import streamlit as st

st.set_page_config(
    page_title="Homepage"
)

st.title("Recipe Reviews & User Feedback Analysis")
st.sidebar.success("Select a page above.")

st.markdown("This analysis is done using the [Recipe Reviews and User Feedback](https://archive.ics.uci.edu/dataset/911/recipe+reviews+and+user+feedback+dataset) dataset from UCI Machine Learning Repository.")