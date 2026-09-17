import json
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)


def load_knowledge_base():

    path = os.path.join(
        BASE_DIR,
        "data",
        "knowledge_base.json"
    )

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def search_knowledge_base(query):

    knowledge_base = load_knowledge_base()

    if not knowledge_base:
        return None, 0.0

    documents = []

    for article in knowledge_base:

        text = (
            article.get("title", "")
            + " "
            + article.get("category", "")
            + " "
            + article.get("policy", "")
            + " "
            + article.get("action", "")
        )

        documents.append(text)


    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words="english"
    )


    document_vectors = vectorizer.fit_transform(
        documents
    )


    query_vector = vectorizer.transform(
        [query]
    )


    similarities = cosine_similarity(
        query_vector,
        document_vectors
    )[0]


    best_index = similarities.argmax()

    score = float(
        similarities[best_index]
    )


    # --------------------------------------------------
    # RELEVANCE THRESHOLD
    # --------------------------------------------------
    # Prevent a completely unrelated request from being
    # shown as if it matched a useful policy.
    #
    # A low score means the knowledge base did not find
    # sufficiently relevant information.
    # --------------------------------------------------

    minimum_similarity = 0.10

    if score < minimum_similarity:

        return None, score


    best_article = knowledge_base[
        best_index
    ]


    return best_article, score