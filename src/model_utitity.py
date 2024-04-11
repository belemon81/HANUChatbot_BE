from src.data_processing import get_embedding
from src.test import client


# def get_cosine_similarity(embedding1, embedding2):
#     return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))


# TODO: Get top most similar documents from the database
def vector_search(query_embedding, conn, table_name):
    with conn.cursor() as cur:
        cur.execute(f'''  
            WITH temp AS (
                SELECT content,
                1-(cosine_distance(embedding,(CAST(%s AS vector)))) as sim
                FROM {table_name}
            )
            SELECT * FROM temp 
            WHERE sim > 0.5
            ORDER BY sim DESC 
            LIMIT 20;
        ''', (query_embedding,))
        top_docs = [(row[0], row[1]) for row in cur.fetchall()]
    return top_docs


# TODO: fetch response from OPENAI client
def get_completion_from_message(messages, model='gpt-4-turbo-2024-04-09', temperature=0, max_tokens=1000):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


def get_answer(question, context, conn, table_name):
    query_embedding = get_embedding(question)
    relevant_docs = vector_search(query_embedding, conn, table_name)

    delimiter = '```'
    user_message = f'{delimiter}{question}{delimiter}'

    if relevant_docs:
        system_message = (
            f'''
                You are a friendly chatbot. \
                You must refer to **Context** first, then **HANU documents**, to answer the questions. \
                You respond in a concise, technically credible tone. \
                You use the language of the question given to respond. \
                You automatically make currency exchange based on the language asked, if not provided specific currency.
            ''' if context else
            f'''
                You are a friendly chatbot. \
                You must refer to **HANU documents** to answer the questions. \
                You respond in a concise, technically credible tone. \
                You use the language of the question given to respond. \
                You automatically make currency exchange based on the language asked, if not provided specific currency.
            ''')
        context_content = f'Context: {context}; ' if context else ''
        assistant = {'role': 'assistant', 'content': f'{context_content}\nHANU documents: {relevant_docs}'}
    else:
        system_message = f'''
                            You are a friendly chatbot. \
                            You respond in a concise, technically credible tone. \
                        '''
        assistant = None

    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message},
        assistant,
    ]

    messages = [message for message in messages if message is not None]

    return get_completion_from_message(messages)
