import os
import requests
import streamlit as st
from openai import AzureOpenAI

# create a config dictionary
config = {
    "endpoint": os.environ["AZURE_OPENAI_ENDPOINT"],
    "api_key": os.environ["AZURE_OPENAI_KEY"],
    "api_version": os.environ["AZURE_OPENAI_API_VERSION"],
    "model": os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
}

# Initialize OpenAI client
clientAOAI = AzureOpenAI(
    azure_endpoint=config["endpoint"],
    api_version=config["api_version"],
    api_key=config["api_key"],
)


# log tracing
def trace(col2, label, message):
    with col2:
        with st.expander(f"{label}:"):
            st.write(message)
            # print(f"{label}: {message}")


# get request api
def get_request(url):
    response = requests.get(url)
    return response.json()


# chat completion
def chat(
    messages=[],
    temperature=0.7,
    max_tokens=800,
    streaming=False,
    format="text",
):
    try:
        # Response generation
        full_response = ""

        for completion in clientAOAI.chat.completions.create(
            model=config["model"],
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=streaming,
            response_format={"type": format},
        ):

            if completion.choices and completion.choices[0].delta.content is not None:
                full_response += completion.choices[0].delta.content

        return full_response

    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None
