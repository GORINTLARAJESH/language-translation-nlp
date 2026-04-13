from flask import Flask, render_template, request, jsonify
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import time

app = Flask(__name__)

history = []

@app.route('/')
def index():
    return render_template('index.html', history=history)

# 🔄 Translation API
@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    text = data['text']
    lang = data['language']

    try:
        translated = GoogleTranslator(source='auto', target=lang).translate(text)

        history.append({
            "input": text,
            "output": translated
        })

        return jsonify({"translated": translated})

    except Exception as e:
        return jsonify({"translated": "Error: " + str(e)})

# 🔊 Google TTS API
@app.route('/speak', methods=['POST'])
def speak():
    data = request.get_json()
    text = data['text']
    lang = data['language']

    try:
        # 🔥 Unique file (avoid caching issue)
        filename = f"output_{int(time.time())}.mp3"
        filepath = os.path.join("static", filename)

        tts = gTTS(text=text, lang=lang)
        tts.save(filepath)

        return jsonify({"audio": f"/static/{filename}"})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)