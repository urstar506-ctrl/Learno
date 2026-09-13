from flask import Flask, send_file, request, jsonify
from pathlib import Path
import os
import json
import urllib.request
import urllib.error

app = Flask(__name__)
BASE = Path(__file__).resolve().parent

@app.route("/")
def home():
    return send_file(BASE / "index.html")

@app.route("/api/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    question = (data.get("question") or "").strip()

    if not question:
        return jsonify({"answer": "Apna question likho."})

    api_key = os.environ.get("GEMINI_API_KEY")

    # API key nahi hai to koi paid/free AI request nahi jayegi
    if not api_key:
        return jsonify({
            "answer": "Learno AI abhi safe demo mode me hai. AI key connect nahi ki gayi hai."
        })

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Tum Learno ke study assistant ho. Student ko simple Hindi me samjhao.\n\nQuestion: " + question
                    }
                ]
            }
        ]
    }

    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        "gemini-2.5-flash:generateContent?key=" + api_key
    )

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))

        answer = result["candidates"][0]["content"]["parts"][0]["text"]
        return jsonify({"answer": answer})

    except Exception:
        return jsonify({
            "answer": "AI se response nahi aa saka. Thodi der baad try karo."
        })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
