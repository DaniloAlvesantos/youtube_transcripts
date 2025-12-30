from flask import Blueprint, jsonify, request
from models.db import DB
from concurrent.futures import ThreadPoolExecutor
from workers.dataset import process_dataset

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")
executor = ThreadPoolExecutor(max_workers=2)

@ai_bp.post("/dataset/<video_id>")
def set_dataset(video_id):
    db = DB().get_collection("transcripts")
    target_tr = db.find_one({ "video_id": video_id })
    
    if not target_tr:
        return jsonify(
            status="Error",
            message="Transcript not found"
        ), 404
    
    current_segments = target_tr["segments"]
    target_lang = "en" if "en" in target_tr["languages"] else target_tr["languages"][0]

    executor.submit(process_dataset, current_segments, target_lang, video_id)

    return jsonify(status="PROCESSING", message="AI is summarizing on background"), 202

@ai_bp.get("/dataset/<video_id>")
def get_dataset(video_id):
    data = DB().get_collection("datasets").find_one({ "video_id": video_id })

    if not data:
        return jsonify(status="Error", message="Dataset not found."), 404
    
    return jsonify(status="OK", data=data), 200