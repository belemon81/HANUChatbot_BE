from flask import Flask, request, jsonify

from src.openai_client import client

app = Flask(__name__)


@app.route('/', methods=['POST'])
def answer_question():
    data = request.get_json()
    question = data.get('question')

    if question:
        try:
            completion = client.chat.completions.create(
                model='gpt-3.5-turbo',
                messages=[
                    {'role': 'user', 'content': question}
                ]
            )
            answer = completion.choices[0].message.content
            return jsonify({'answer': answer})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Question not provided.'}), 400


if __name__ == '__main__':
    app.run(host='localhost', port=2305)
