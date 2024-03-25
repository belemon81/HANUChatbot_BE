import os

import psycopg2
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify
from openai import OpenAI

from src.model_utitity import get_answer

app = Flask(__name__)
_ = load_dotenv(find_dotenv())
openai_api_key = os.environ['OPENAI_API_KEY']
client = OpenAI(api_key=openai_api_key)
conn = psycopg2.connect(database='hanu_chatbot', user='postgres', password='postgres', host='localhost', port=23050)
cache_data = []


@app.route('/hanu-chatbot/educational-program', methods=['POST'])
def answer_educational_program_question():
    data = request.get_json()
    question = data.get('question')
    context = data.get('context')

    if question:
        try:
            answer = get_answer(question, context, conn, 'embeddings')  # TODO: change name
            # save_to_cache(answer)
            return jsonify({'answer': answer})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Question not provided!'}), 400


@app.route('/hanu-chatbot/events-clubs', methods=['POST'])
def answer_events_clubs_question():
    data = request.get_json()
    question = data.get('question')
    context = data.get('context')

    if question:
        try:
            answer = get_answer(question, context, conn, 'events-clubs')
            # save_to_cache(answer)
            return jsonify({'answer': answer})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Question not provided!'}), 400


if __name__ == '__main__':
    app.run(host='localhost', port=2305)
