from flask import Flask, jsonify
from models.transcript import Transcript

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify(status="ok"), 200

@app.post("/transcript/<id>")
def transcript(id):
    transcript = Transcript(video_id=id, language="pt")
    transcript.fetch_transcription()

    if not len(transcript.segments):
         return jsonify(error="Transcript not found"), 404

    transcript.save_to_file(path="./")

    return jsonify(id=id, status="created"), 201
