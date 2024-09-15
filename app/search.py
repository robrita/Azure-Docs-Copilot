import json
import streamlit as st
import app.utils as utils
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load the model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# get user query
def query():
    category, question, submit, threshold, top_n = select_options()
    print(">>>>>question:", question)

    if submit:
        with st.spinner("Processing ..."):
            try:
                url = f"https://learn.microsoft.com/api/search?search={question}&locale=en-us&facet=category&facet=products&%24filter=(category%20eq%20%27{category}%27)&%24top=10&expandScope=true&includeQuestion=false&applyOperator=false&partnerId=LearnSite"
                # check for category
                if category == "All":
                    url = f"https://learn.microsoft.com/api/search?search={question}&locale=en-us&facet=category&facet=products&%24top=10&expandScope=true&includeQuestion=false&applyOperator=false&partnerId=LearnSite"

                # print(">>>>>url", url)
                contents = search_docs(url)
                results = vector_search(question, contents, threshold, top_n)

                # print(">>>>>results", results)
                format_results(results)

            except Exception as e:
                st.error(f"error in query(): {e}")


# select user options
def select_options():
    categories = {
        "Documentation": "Documentation",
        "Training": "Training",
        "Credentials": "Credential",
        "Q&A": "QnA",
        "Reference": "Reference",
        "Shows": "Show",
        "All": "All",
    }

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            # provide options for user to select category
            selected_category = st.selectbox(
                "Category:", options=list(categories.keys())
            )
            category = categories[selected_category]

            question = st.text_input("Enter your query: ", key="input")
            submit = st.button("Search", key="submit", disabled=question == "")

        with col2:
            threshold = st.selectbox(
                "Threshold:", [0.8, 0.7, 0.6, 0.5, 0.4, 0.3], index=3
            )
            top_n = st.selectbox("TopK:", [3, 4, 5, 6, 7, 8, 9, 10])

        # show relevant queries
        if submit:
            st.markdown("**Relevant queries:**")
            queries = relevant_queries(question)
            st.write(queries[0])
            st.write(queries[1])
            st.write(queries[2])

    return category, question, submit, threshold, top_n


# get relevant queries
def relevant_queries(query):
    system = [
        "given a search query below, rewrite it into 3 different effective search queries with complete thought.",
        "Return in json format under the rewrite key.\n",
        f"query: {query}",
        f"rewrite:",
    ]

    messages = [
        {"role": "system", "content": "\n".join(system)},
    ]
    result = utils.chat(messages, 0.7, 400, True, "json_object")
    # print(">>>>>result", result)
    return json.loads(result)["rewrite"]


# get query results
def search_docs(url):
    data = utils.get_request(url)
    contents = []
    # st.write(data)

    # throw error if no results
    if not data["results"]:
        raise Exception("No results found:")

    # st.write(data["results"])
    # loop through all the results
    for result in data["results"]:
        # st.write(result)
        results = [result["title"], result["url"], result["description"]]
        # append to list
        contents.append(json.dumps(results))

    return contents


# Define a function for vector search
def vector_search(query, contents, threshold=0.5, top_n=3):
    # Encode the contents and query
    embeddings = model.encode(contents)
    query_embedding = model.encode([query])

    # Compute cosine similarity between the query and each sentence
    similarities = cosine_similarity(query_embedding, embeddings).flatten()

    # Get top N results that cross the threshold
    top_indices = np.where(similarities > threshold)[0]
    sorted_indices = top_indices[np.argsort(similarities[top_indices])[::-1]]
    # print(">>>>>sorted_indices", sorted_indices)

    # Return the top N results
    results = [(contents[i], similarities[i]) for i in sorted_indices[:top_n]]
    # throw error if no results
    if not results:
        raise Exception("No results found: Try changing the threshold or topK value.")

    return results


# format results
def format_results(results):
    # loop through all the results
    for result in results:
        # print(">>>>>result", result)
        result_json = json.loads(result[0])

        # display results
        with st.container(border=True):
            st.markdown(f"##### [{result_json[0]}]({result_json[1]}) ({result[1]:.3f})")
            st.write(result_json[2])
