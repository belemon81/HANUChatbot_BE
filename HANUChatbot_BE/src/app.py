import psycopg2
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

from data_processing import get_embedding
from model_utitity import get_answer, vector_search

app = Flask(__name__)
cors = CORS(app, origins=['http://localhost:3000'])
conn = psycopg2.connect(user='postgres', password='postgres', host=os.environ.get("DB_HOST"), port=5432)


@app.route('/', methods=['GET'])
def check_app_health():
    return jsonify({'status': 'OK'})


@app.route('/hanu-chatbot/educational-program', methods=['POST'])
def get_educational_program_details():
    data = request.get_json()
    question = data.get('question')
    # context = data.get('context')

    if question:
        try:
            query_embedding = get_embedding(question)
            relevant_docs = vector_search(query_embedding, conn, 'educational_program')
            return jsonify({'relevant_docs': relevant_docs})
            # answer = get_answer(question, context, conn, 'educational_program')
            # return jsonify({'answer': answer})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Question not provided!'}), 400


@app.route('/hanu-chatbot/public-administration', methods=['POST'])
def get_public_administration_details():
    data = request.get_json()
    question = data.get('question')
    # context = data.get('context')

    if question:
        try:
            # answer = get_answer(question, context, conn, 'public_administration')
            # return jsonify({'answer': answer})
            query_embedding = get_embedding(question)
            relevant_docs = vector_search(query_embedding, conn, 'public_administration')
            return jsonify({'relevant_docs': relevant_docs})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Question not provided!'}), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)  # old: localhost
