import psycopg2
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from data_processing import get_embedding
from model_utitity import get_answer, vector_search

load_dotenv()

app = Flask(__name__)
cors = CORS(app, origins=os.environ.get("CORS_ORIGINS", "http://localhost:3000").split(","))
conn = psycopg2.connect(
    user=os.environ.get("DB_USER", "postgres"),
    password=os.environ.get("DB_PASSWORD", "postgres"),
    host=os.environ.get("DB_HOST", "localhost"),
    port=int(os.environ.get("DB_PORT_MAIN", "5433")),
)


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
    app.run(
        host=os.environ.get("FLASK_HOST", "0.0.0.0"),
        port=int(os.environ.get("FLASK_PORT", "8080")),
    )  # old: localhost
