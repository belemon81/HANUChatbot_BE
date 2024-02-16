from flask import Flask, request, jsonify
from src.data_collecting import collect_data
from src.data_processing import get_embedding
from openai import OpenAI
import numpy as np
import os
from dotenv import load_dotenv, find_dotenv

app = Flask(__name__)
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ['API_KEY']
client = OpenAI(api_key=openai_api_key)


def cosine_similarity(embedding1, embedding2):
    return np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))


def search_pipeline(documents, description, n=3, pprint=True):
    embedding = get_embedding(description, model='text-embedding-3-small')
    similarities = [cosine_similarity(get_embedding(doc), embedding) for doc in documents]
    res = [(index, similarity) for index, similarity in
           sorted(enumerate(similarities), key=lambda x: x[1], reverse=True)][:n]
    if pprint:
        for index, similarity in res:
            print(f"Document {index + 1}: Similarity = {similarity:.4f}")
    return res


@app.route('/', methods=['POST'])
def answer_question():
    data = request.get_json()
    question = data.get('question')

    if question:
        try:
            documents = collect_data()
            res = search_pipeline(documents, question, n=1, pprint=False)
            doc = collect_data()[res[0][0]]
            return jsonify({'answer': doc})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Question not provided'}), 400


if __name__ == '__main__':
    app.run(host='localhost', port=2304)
