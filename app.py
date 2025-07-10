from flask import Flask, request, jsonify
from flask_cors import CORS
from gtts import gTTS
import os
from datetime import datetime

app = Flask(__name__)

# ✅ CORS Fix: Only allow your frontend domain
CORS(app, resources={r"/*": {"origins": "https://carrierbanao.carrierbanao.com"}})

# 🔧 MP3 save path (inside static/mp3)
SAVE_DIR = "static/mp3"
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route("/")
def home():
    return "TTS API is running!"

@app.route("/generate", methods=["POST"])
def generate_audio():
    data = request.get_json()

    text = data.get("text")
    lang = data.get("lang", "en")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        # 📁 Generate unique filename
        filename = f"tts_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
        filepath = os.path.join(SAVE_DIR, filename)

        # 🎤 Generate speech
        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)

        # ✅ Return relative path to mp3
        return jsonify({"url": f"/static/mp3/{filename}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
