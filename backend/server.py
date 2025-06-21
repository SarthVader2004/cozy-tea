from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read API key securely
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)
CORS(app)

@app.route('/recommend', methods=['POST'])
def recommend_tea():
    mood = request.json.get("mood", "")
    if not mood:
        return jsonify({"error": "No mood provided."}), 400

    # AI Prompt to send to Groq
    prompt = f"I feel {mood}. Recommend me a tea in this format:\n" \
             "✨ Name:\n🍃 Ingredients:\n💖 Benefit:"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama-3.3-70b-versatile",  # Updated model name from Groq docs
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        print("Status code:", response.status_code)
        print("Response text:", response.text)

        if response.status_code != 200:
            return jsonify({"error": f"API request failed: {response.text}"}), 500

        result = response.json()
        ai_response = result['choices'][0]['message']['content']
        return jsonify({"response": ai_response.strip()})
    except Exception as e:
        print("❌ Error:", e)
        return jsonify({"error": "Something went wrong."}), 500

@app.route('/')
def home():
    return "Backend is up and running!"

if __name__ == '__main__':
    app.run(debug=True)
