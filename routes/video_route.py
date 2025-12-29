from flask import Blueprint, jsonify
from models.transcript import Transcript
from models.yt import YT
from models.db import DB
from concurrent.futures import ThreadPoolExecutor

video_bp = Blueprint("video", __name__, url_prefix="/video")
executor = ThreadPoolExecutor(max_workers=3)

def background_process(video_id):
    db = DB().get_collection("transcripts")
    try:
        db.update_one({"video_id": video_id}, {"$set": {"status": "downloading"}}, upsert=True)
        
        yt = YT(video_id)
        
        db.update_one({"video_id": video_id}, {"$set": {"status": "transcribing"}})
        
        tr = Transcript(video_id)
        tr._language = {"lan": yt.detected_language}        
        tr._segments = yt.transcript

        tr.save()
        
    except Exception as e:
        db.update_one({"video_id": video_id}, {"$set": {"status": "error", "error_msg": str(e)}})

@video_bp.get("/<video_id>")
def get_video_status(video_id):
    db = DB().get_collection("transcripts")
    doc = db.find_one({"video_id": video_id})

    if not doc:
        executor.submit(background_process, video_id)
        return jsonify(
            status="PROCESSING", 
            message="Transcription started.", 
            video_id=video_id
        ), 202

    current_status = doc.get("status", "pending")
    
    return jsonify(
        status=current_status,
        video_id=video_id,
        data=doc.get("segments") if current_status == "completed" else None
    ), 200