import json

import numpy as np

from src.data_processing import get_embedding
from src.test import client


def cosine_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))


def search_pipeline(documents, question, n=2):
    embedding = get_embedding(question)
    similarities = [cosine_similarity(get_embedding(doc), embedding) for doc in documents]
    res = [(index, similarity) for index, similarity in
           sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)][:n]
    return res


# Helper function: Get top most similar documents from the database
def get_top_similar_docs(query_embedding, conn):
    with conn.cursor() as cur:
        cur.execute("""  
            SELECT content, cosine_distance(embedding, %s) AS cosim FROM embeddings   
            ORDER BY cosim LIMIT 2
        """, (json.dumps(query_embedding),))
        top_docs = cur.fetchall()
    return top_docs


def get_completion_from_message(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=1000):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def get_answer(question, conn, related_docs):
    if not related_docs:
        related_docs = get_top_similar_docs(get_embedding(question), conn)
    else:
        related_docs = related_docs.append(get_top_similar_docs(get_embedding(question), conn))
    if related_docs:
        delimiter = "```"
        system_message = """
                                You are a friendly chatbot. \
                                You can answer questions about relevant information. \
                                You respond in a concise, technically credible tone. \
                            """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"{delimiter}{question}{delimiter}"},
            {"role": "assistant",
             "content": f"Relevant information:\n {related_docs}"}
        ]
    else:
        messages = [
            {"role": "user", "content": question}
        ]
    return get_completion_from_message(messages)
