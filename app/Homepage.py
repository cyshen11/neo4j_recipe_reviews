import streamlit as st

st.set_page_config(
    page_title="Homepage"
)

st.title("Recipe Reviews & User Feedback Analysis")
st.sidebar.success("Select a page above.")

st.markdown("""
A comprehensive tool for analyzing recipe reviews and user feedback. This application provides business with actionable insights into user behavior, helping them make data-driven decisions.

### Key Features:

- **Influential Commenter Analysis**: Analyze the reach of high-reputation user's comments
- **Recipe Similarity**: Discover recipes that attract a similar audience
- **User Recipe Commenting Paths**: Map the typical journey a user takes when commenting on recipes
- **Chain of Influence**: Measures high-reputation user's indirect influence on recipe's overall engagement
- **Recipe Journey**: Commenting journey of a new user
- **Impact of High Rated Comments**: Measure how does a 5-star comment from a high-reputation user affect subsequent commenting activity on a recipe

---

### How to Use:

Select a page other than the homepage to view its analysis.

---

### Tech Stack:

- Frontend:
  - Streamlit
- Backend:
  - Database: Neo4J
- Cloud Services:
  - Streamlit Community Cloud
  - Neo4J Aura

---

### Credits:

- Credits to UCI Machine Learning Repository for the [Recipe Reviews and User Feedback](https://archive.ics.uci.edu/dataset/911/recipe+reviews+and+user+feedback+dataset) dataset

---

Developed by Vincent Cheng  
<a href="https://www.linkedin.com/in/yun-sheng-cheng-86094a143/" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" alt="LinkedIn" style="height:30px; width:30px;filter: grayscale(100%);">
</a>
""", unsafe_allow_html=True)