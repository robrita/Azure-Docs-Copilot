import streamlit as st
import app.pages as pages
import app.search as search

# App home page
pages.show_home()

search.query()

# app sidebar
with st.sidebar:
    st.image(
        "https://github.com/robrita/Azure-Docs-Copilot/blob/main/img/azure-docs.png?raw=true"
    )
    st.write(
        "Azure Docs Copilot aims to enhance productivity and efficiency for developers and architects by providing a reliable and quick way to access the latest information from Azure documentation."
    )

    st.subheader("🛠Technology Stack", anchor=False)
    st.write("Python, Streamlit, Azure OpenAI")
    st.write(
        "Repo: [Azure Docs Copilot](https://github.com/robrita/Azure-Docs-Copilot)"
    )
