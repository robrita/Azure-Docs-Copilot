import streamlit as st
import app.pages

# App home page
app.pages.show_home()

# app sidebar
with st.sidebar:
    st.write("These AI app use cases are all powered by Azure OpenAI.")
    st.divider()

    st.subheader("🛠Technology Stack", anchor=False)
    st.write("Python, Streamlit, Azure OpenAI, Azure AI Search")
    st.write(
        "Check out the repo here: [Azure AI Apps](https://github.com/robrita/awesome-azure-ai-apps)"
    )
