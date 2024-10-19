from sklearn.metrics.pairwise import cosine_similarity
import app.utils as utils
import numpy as np


# vector reranking
def vector_rerank(query, contents, threshold=0.5, top_n=3):
    # Encode the contents and query
    query_embedding = utils.get_embeddings([query])
    embeddings = utils.get_embeddings(contents)

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
