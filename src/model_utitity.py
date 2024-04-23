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
            WHERE sim > 0.3
            ORDER BY sim DESC 
            LIMIT 15;
        ''', (query_embedding,))
        top_docs = [row[0] for row in cur.fetchall()]
        # top_docs = [(row[0], row[1]) for row in cur.fetchall()]
    return top_docs


# TODO: customize response
def get_answer(question, context, conn, table_name):
    query_embedding = get_embedding(question)
    relevant_docs = vector_search(query_embedding, conn, table_name)
    delimiter = '```'
    user_message = f'{delimiter}{question}{delimiter}'
    if relevant_docs:
        system_message = (f'''
            You are a friendly chatbot of Hanoi University. \
            {('You must refer to HISTORY (your previous responses) for understanding the question if necessary. ' 
            if context else '')} \
            You must filter all relevant content in HANU documents to answer the questions. \
            You use the language of the question to respond. \
            You respond with a concise, technically credible tone. \
            You automatically make currency exchange based on the language asked, if not provided specific currency.
        ''')
        context_content = f'HISTORY:\n {context}; ' if context else ''
        assistant = {'role': 'assistant', 'content': f'{context_content}\nHANU documents:\n {relevant_docs}'}
    else:
        system_message = f'''
                            You are a friendly chatbot. \
                            You use the language of the question to respond. \
                            You respond in a concise, technically credible tone. 
                        '''
        assistant = None
    messages = [
        {'role': 'system', 'content': system_message},
        {'role': 'user', 'content': user_message},
        assistant,
    ]
    messages = [message for message in messages if message is not None]
    return get_completion_from_messages(messages)


# TODO: fetch response from OPENAI client
def get_completion_from_messages(messages, model='gpt-3.5-turbo-0125', temperature=0, max_tokens=1500):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content


