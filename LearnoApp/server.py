from flask import Flask, send_file, request, jsonify
from pathlib import Path

app = Flask(__name__)
BASE = Path(__file__).resolve().parent

@app.route('/')
def home():
    return send_file(BASE / 'index.html')

@app.route('/api/ask', methods=['POST'])
def ask():
    data = request.get_json(silent=True) or {}
    question = (data.get('question') or '').strip()
    if not question:
        return jsonify({'answer': 'Apna question likho.'})
    return jsonify({'answer': 'Learno AI abhi demo mode me hai. Real AI baad me secure aur limited-cost setup ke saath connect karenge.'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=False)
