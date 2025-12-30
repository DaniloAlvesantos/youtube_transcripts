from models.transcript import Transcript
from models.yt import YT
from models.db import DB

def background_process(video_id):
    db = DB().get_collection("transcripts")
    try:
        db.update_one({"video_id": video_id}, {"$set": {"status": "downloading"}}, upsert=True)
        
        yt = YT(video_id)
        
        tr = Transcript(video_id)
        tr._language = {"lan": yt.detected_language}        
        tr._segments = yt.transcript

        tr.save()
        
    except Exception as e:
        db.update_one({"video_id": video_id}, {"$set": {"status": "error", "error_msg": str(e)}})

    print(f"Processing/Transcript video {video_id} has done")