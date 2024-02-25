import os
import psycopg2

from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify
from openai import OpenAI

from src.data_collecting import collect_data
from src.data_processing import process_data
from src.data_searching import get_answer, search_pipeline

app = Flask(__name__)
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=openai_api_key)
conn = psycopg2.connect(database="hanu_chatbot", user="postgres", password="postgres", host="localhost",
                        port=23050)
process_data('../documents/embedded_test.csv', '../documents/embedded_test.csv')


@app.route('/', methods=['POST'])
def answer_question():
    data = request.get_json()
    question = data.get('question')

    if question:
        try:
            documents = collect_data('../documents/new_test.csv')
            res = search_pipeline(documents, question)
            doc = documents[res[0][:2]]
            answer = get_answer(question, conn)
            return jsonify({'answer': answer})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Question not provided!'}), 400


if __name__ == '__main__':
    app.run(host='localhost', port=2305)
