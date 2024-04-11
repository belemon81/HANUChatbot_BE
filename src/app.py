import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

from src.data_processing import get_embedding
from src.model_utitity import vector_search, get_answer

app = Flask(__name__)
cors = CORS(app, origins=['http://localhost:3000'])
conn = psycopg2.connect(database='hanu_chatbot', user='postgres', password='postgres', host='localhost', port=23050)


@app.route('/', methods=['GET'])
def check_app_health():
    return jsonify({'status': 'OK'})


@app.route('/hanu-chatbot/educational-program', methods=['POST'])
def answer_educational_program_question():
    data = request.get_json()
    question = data.get('question')
    context = data.get('context')

    if question:
        try:
            answer = get_answer(question, context, conn, 'test')
            return jsonify({'answer': answer})
            # query_embedding = get_embedding(question)
            # relevant_docs = vector_search(query_embedding, conn, 'test')
            # return jsonify({'relevant_docs': relevant_docs})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Question not provided!'}), 400


@app.route('/hanu-chatbot/public-administration', methods=['POST'])
def answer_events_clubs_question():
    data = request.get_json()
    question = data.get('question')
    # context = data.get('context')

    if question:
        try:
            # answer = get_answer(question, context, conn, 'public-administration')
            # return jsonify({'answer': answer})
            query_embedding = get_embedding(question)
            relevant_docs = vector_search(query_embedding, conn, 'public-administration')
            return jsonify({'relevant_docs': relevant_docs})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Question not provided!'}), 400


if __name__ == '__main__':
    app.run(host='localhost', port=2305)
