from flask import Flask, jsonify, render_template, request
from models.transcript import Transcript
from models.db import DB
from models.yt import YT

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("/home/home.html")


# ---------------------------
# GET ALL TRANSCRIPTS
# ---------------------------
@app.get("/transcript/all")
def get_all_transcripts():
    cursor = DB().get_collection("transcripts").find()

    data = []
    for doc in cursor:
        doc["_id"] = str(doc["_id"])
        data.append(doc)

    return jsonify(status="OK", data=data), 200


# ---------------------------
# GET TRANSCRIPT BY VIDEO ID
# ---------------------------
@app.get("/transcript/<video_id>")
def get_transcript_by_id(video_id):
    if not video_id:
        return jsonify(
            status="ERROR",
            message="video_id is required"
        ), 400

    db = DB()
    data = db.get_collection("transcripts").find_one({
        "video_id": video_id
    })

    if not data:
        return jsonify(
            status="ERROR",
            message="Transcript not found"
        ), 404

    # 🔑 convert ObjectId
    data["_id"] = str(data["_id"])

    return jsonify(
        status="OK",
        data=data
    ), 200


# ---------------------------
# CREATE TRANSCRIPT (DB)
# ---------------------------
@app.post("/transcript/<video_id>")
def create_transcript(video_id):
    tr = Transcript(video_id=video_id)
    tr.fetch_transcription()

    if not tr.segments:
        return jsonify(error="Transcript not found"), 404

    tr.save()
    return jsonify(id=video_id, status="created", data=tr.to_dict()), 201


# ---------------------------
# CREATE TRANSCRIPT (JSON FILE)
# ---------------------------
@app.post("/transcript/<video_id>/json")
def create_transcript_json(video_id):
    tr = Transcript(video_id=video_id)
    tr.fetch_transcription()

    if not tr.segments:
        return jsonify(error="Transcript not found"), 404

    tr.save_to_file(path="./")
    return jsonify(id=video_id, status="created"), 201

# @app.post("/transcript/<v")

@app.get("/video/<video_id>")
def download_video(video_id):
    yt = YT(video_id)
    tr = Transcript(video_id)
    tr._language = tr._select_language(yt)
    tr._segments = yt.transcript

    data = tr.save()

    return jsonify(status="OK", data = yt.transcript), 200