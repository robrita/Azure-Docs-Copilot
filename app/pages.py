import streamlit as st


def show_home():
    st.set_page_config(
        page_title="Azure Docs Copilot",
        page_icon="✨",
        layout="wide",
        # initial_sidebar_state="collapsed",
    )

    st.logo(
        "https://swimburger.net/media/ppnn3pcl/azure.png",
        link="https://ai.azure.com/",
    )
    st.title("✨Azure Docs Copilot")

    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            # padding-bottom: 1rem;
            # padding-left: 1rem;
            # padding-right: 1rem;
        }
        .stAppDeployButton {
            display: none;
        }
        .st-emotion-cache-15ecox0 {
            display: none;
        }
        .viewerBadge_container__r5tak {
            display: none;
        }
        .styles_viewerBadge__CvC9N {
            display: none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
