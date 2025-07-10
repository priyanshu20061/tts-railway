from flask import Flask, request, jsonify
from flask_cors import CORS
from gtts import gTTS
import os, time

app = Flask(__name__)
CORS(app)

STATIC_DIR = "static/mp3"
os.makedirs(STATIC_DIR, exist_ok=True)

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    text = (data.get("text", "") or "").strip()
    lang = data.get("lang", "en")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    filename = f"tts_{int(time.time())}.mp3"
    filepath = os.path.join(STATIC_DIR, filename)

    try:
        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"url": f"/{STATIC_DIR}/{filename}"})
