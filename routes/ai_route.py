from flask import Blueprint, jsonify, request
from models.db import DB
from models.ai import AI
from concurrent.futures import ThreadPoolExecutor

ai_bp = Blueprint("ai", __name__, url_prefix="/ai")
executor = ThreadPoolExecutor(max_workers=2)

@ai_bp.get("/dataset/<video_id>")
def generate_dataset(video_id):
    db = DB().get_collection("transcripts")
    target_tr = db.find_one({ "video_id": video_id })
    
    if not target_tr:
        return jsonify(
            status="Error",
            message="Transcript not found"
        ), 404
    
    ai = AI()
    current_segments = target_tr["segments"]
    target_lang = "en" if "en" in target_tr["languages"] else target_tr["languages"][0]

    summarize = ai.summarize_preaching(segments=current_segments, lang=target_lang)
    print(summarize)
    return jsonify(status="OK"), 200