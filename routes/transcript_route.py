from flask import Blueprint, jsonify, request
from models.transcript import Transcript
from models.db import DB
from workers.translate import translate_worker
from concurrent.futures import ThreadPoolExecutor

transcript_bp = Blueprint("transcript", __name__, url_prefix="/transcript")
executor = ThreadPoolExecutor(max_workers=3)

@transcript_bp.get("/all")
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
@transcript_bp.get("/<video_id>")
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
@transcript_bp.post("/<video_id>")
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
@transcript_bp.post("/<video_id>/json")
def create_transcript_json(video_id):
    tr = Transcript(video_id=video_id)
    tr.fetch_transcription()

    if not tr.segments:
        return jsonify(error="Transcript not found"), 404

    tr.save_to_file(path="./")
    return jsonify(id=video_id, status="created"), 

@transcript_bp.get("/translate/<video_id>/<target_lang>")
def translate_transcript(video_id, target_lang="en"):
    db = DB().get_collection("transcripts")
    doc = db.find_one({"video_id": video_id})

    if not doc:
        return jsonify(status="Error", message="Transcript not found!"), 404
    
    available_langs = doc.get("languages", [])
    if target_lang in available_langs:
        return jsonify(status="OK", message="Already translated", data=doc.get("segments")), 200

    db.update_one({"video_id": video_id}, {"$set": {"status": "translating"}})
    
    executor.submit(translate_worker, video_id, target_lang)

    return jsonify(
        status="PROCESSING", 
        message=f"Translation to {target_lang} started.", 
        video_id=video_id
    ), 202