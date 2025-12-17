import os
import json
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from .thumb import Thumb

class Transcript:
    def __init__(self, video_id, language):
        self._video_id = video_id
        self._language = language
        self._segments = []
        self._thumb = None
    
    def fetch_transcription(self):
        self._segments = []

        try: 
            yt = YouTubeTranscriptApi()
            yt_response = yt.fetch(self._video_id, languages=[self._language])

            for chunk in yt_response:
                self._segments.append({
                    "text": chunk.text,
                    "start": chunk.start,
                    "duration": chunk.duration
                })

        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
            print(f"Error acurred: {e}")
    
    @property
    def video_id(self):
        return self._video_id

    @property
    def language(self):
        return self._language

    @property
    def segments(self):
        return self._segments

    def to_json(self):
        if not self._segments:
            raise ValueError("Transcript not fetched or empty")
        
        thumb = Thumb(self._video_id)
        thumb_url = thumb.extract_thumb()

        return {
            "video_id": self._video_id,
            "language": self._language,
            "thumb": thumb_url or "",
            "segments": self._segments
        }

    def save_to_file(self, path: str):
        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, f"{self._video_id}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_json(), f, ensure_ascii=False, indent=4)

    def __str__(self):
        return (
            f"Transcript(video_id={self._video_id}, "
            f"language={self._language}, "
            f"segments_count={len(self._segments)})"
        )