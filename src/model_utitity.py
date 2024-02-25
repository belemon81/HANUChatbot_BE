import json

import numpy as np
import pandas as pd

from src.data_processing import get_embedding
from src.test import client


def cosine_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))


def pipeline_search(query_embedding, n=2):
    new_data = pd.read_csv('../documents/new_embedded_test.csv')
    similarities = []
    for index, row in new_data.iterrows():
        row_embedding = np.array(eval(row['Embedding']))
        similarity = cosine_similarity(row_embedding, query_embedding)
        similarities.append(similarity)
    indexes = [index for index, _ in sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)][:n]
    result = []
    for index in indexes:
        result.append(new_data.Combined[index])
    return result


# Get top most similar documents from the database
def vector_search(query_embedding, conn):
    with conn.cursor() as cur:
        cur.execute("""  
            SELECT content FROM embeddings   
            ORDER BY cosine_distance(embedding, %s) LIMIT 2
        """, (json.dumps(query_embedding),))
        top_docs = [row[0] for row in cur.fetchall()]
    return top_docs


def get_completion_from_message(messages, model="gpt-3.5-turbo", temperature=0, max_tokens=1000):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def get_answer(question, conn):
    query_embedding = get_embedding(question)
    new_related_docs = pipeline_search(query_embedding)
    related_docs = new_related_docs + vector_search(query_embedding, conn)
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
            {"role": "assistant", "content": f"Relevant information:\n {related_docs}"}
        ]
    else:
        messages = [
            {"role": "user", "content": question}
        ]
    return get_completion_from_message(messages)