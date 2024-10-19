import json
import streamlit as st
import app.utils as utils
import app.reranker as reranker


# get user query
def query():
    category, question, submit, threshold, top_n = select_options()
    # print(">>>>>question:", question)

    if submit:
        with st.spinner("Processing ..."):
            try:
                url = f"https://learn.microsoft.com/api/search?search={question}&locale=en-us&facet=category&facet=products&%24filter=(category%20eq%20%27{category}%27)&%24top=10&expandScope=true&includeQuestion=false&applyOperator=false&partnerId=LearnSite"
                # check for category
                if category == "All":
                    url = f"https://learn.microsoft.com/api/search?search={question}&locale=en-us&facet=category&facet=products&%24top=10&expandScope=true&includeQuestion=false&applyOperator=false&partnerId=LearnSite"

                # print(">>>>>url", url)
                contents = search_docs(url)
                results = reranker.vector_rerank(question, contents, threshold, top_n)

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
            threshold = st.selectbox("Threshold:", [0.2, 0.5, 0.8], index=1)
            top_n = st.selectbox("TopK:", [5, 10])

        # show relevant queries
        if submit:
            st.markdown("**Relevant queries:**")
            queries = relevant_queries(question)
            st.write(queries[0])
            st.write(queries[1])
            st.write(queries[2])

    return category, question, submit, threshold, top_n


# get relevant queries
@st.cache_data
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
    result = utils.chat(messages, 0.7, 400, True, "json_object", "gpt-4o-mini")
    # print(">>>>>result", result)
    return json.loads(result)["rewrite"]


# get query results
@st.cache_data
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


# format results
@st.cache_data
def format_results(results):
    # loop through all the results
    for result in results:
        # print(">>>>>result", result)
        result_json = json.loads(result[0])

        # display results
        with st.container(border=True):
            st.markdown(f"##### [{result_json[0]}]({result_json[1]}) ({result[1]:.3f})")
            st.write(result_json[2])
