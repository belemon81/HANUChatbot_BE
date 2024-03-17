from src.data_processing import get_embedding
from src.test import client

# def get_cosine_similarity(embedding1, embedding2):
#     return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
#

# def search_from_fresh_data(query_embedding, n=10):
#     new_data = pd.read_csv('../documents/new_embedded_test.csv')
#     similarities = []
#     for index, row in new_data.iterrows():
#         row_embedding = np.array(eval(row['Embedding']))
#         similarity = get_cosine_similarity(row_embedding, query_embedding)
#         similarities.append(similarity)
#     indexes = [index for index, _ in sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)][:n]
#     result = []
#     for index in indexes:
#         result.append(new_data.Combined[index])
#     return result

cache = []


# TODO: cache utility
def save_to_cache(answer):
    global cache
    if len(cache) == 2:
        cache.pop()
    cache = [answer] + cache
    print(cache)


# Get top most similar documents from the database
def vector_search(query_embedding, conn):
    with conn.cursor() as cur:
        cur.execute("""  
            WITH temp AS (
                SELECT content,
                1-(cosine_distance(embedding,(CAST(%s AS vector)))) as sim
                FROM embeddings
            )
            SELECT * FROM temp 
            WHERE sim > 0.5
            ORDER BY sim DESC 
            LIMIT 5;
        """, (query_embedding,))
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
    global cache
    query_embedding = get_embedding(question)
    # new_related_docs = search_from_fresh_data(query_embedding)
    relevant_docs = vector_search(query_embedding, conn)
    if relevant_docs:
        delimiter = "```"
        system_message = f"""
                            You are a friendly chatbot. \
                            You must refer to **HANU documents** to answer the questions \
                            You respond in a concise, technically credible tone. \
                         """

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"{delimiter}Context: {cache}; {question}{delimiter}"},
            {"role": "assistant", "content": f"HANU documents:\n{relevant_docs}"}
        ]

    else:
        messages = [
            {"role": "user", "content": question}
        ]
    return get_completion_from_message(messages)
