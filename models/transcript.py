import os
import json
from typing import Optional, List, Dict

from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)

from .thumb import Thumb
from .db import DB


class Transcript:
    """
    GET OR CREATE TRANSCRIPTS
    FROM YOUTUBE VIDEOS
    """
    def __init__(self, video_id: str):
        if not video_id:
            raise ValueError("video_id is required")

        self._video_id: str = video_id
        self._language: Optional[Dict] = None
        self._segments: List[Dict] = []
        self._thumb: Optional[str] = None

    def fetch_transcription(self) -> None:
        """
        Fetch transcript from DB or YouTube.
        DB has priority (idempotent behavior).
        """
        self._segments = []

        cached = self._load_from_db()
        if cached:
            return

        try:
            yt = YouTubeTranscriptApi()
            self._language = self._select_language(yt)

            if not self._language:
                raise NoTranscriptFound("No generated transcript available")

            yt_response = yt.fetch(
                self._video_id,
                languages=[self._language["lan"]],
            )

            self._segments = [
                {
                    "text": chunk.text,
                    "start": chunk.start,
                    "duration": chunk.duration,
                }
                for chunk in yt_response
            ]

        except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable) as e:
            print(f"[Transcript] Fetch error: {e}")

    @property
    def video_id(self) -> str:
        return self._video_id

    @property
    def language(self) -> Optional[Dict]:
        return self._language

    @property
    def segments(self) -> List[Dict]:
        return self._segments

    def save(self):
        if not self._segments:
            raise ValueError("Transcript not fetched or empty")

        db = DB().get_collection("transcripts")
    
        return db.update_one(
            {"video_id": self._video_id},
            {"$set": self.to_dict()},
            upsert=True
        )

    def save_to_file(self, path: str):
        if not self._segments:
            raise ValueError("Transcript not fetched or empty")

        os.makedirs(path, exist_ok=True)
        file_path = os.path.join(path, f"{self._video_id}.json")

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=4)

        return file_path

    def to_dict(self) -> Dict:
        thumb_url = self._thumb or Thumb(self._video_id).extract_thumb()
    
        formatted_segments = []
        for s in self._segments:
            start = s.get("start", 0)
            end = s.get("end") or (start + s.get("duration", 0))
        
            lang_code = self._language.get("lan") if self._language else "unknown"

            formatted_segments.append({
                "start": start,
                "end": end,
                "text": {
                    lang_code: s.get("text", "")
                }
            })

        return {
         "video_id": self._video_id,
            "languages": [lang_code],
            "thumb": thumb_url or "",
            "segments": formatted_segments,
            "status": "completed"
        }

    def _load_from_db(self) -> bool:
        """
        Load transcript from DB if exists.
        Returns True if loaded.
        """
        data = self.search_on_db()
        if not data:
            return False

        self._language = data.get("language")
        self._segments = data.get("segments", [])
        self._thumb = data.get("thumb")

        print("[Transcript] Loaded from DB")
        return True

    def _exists_in_db(self) -> bool:
        return self.search_on_db() is not None

    def search_on_db(self) -> Optional[Dict]:
        db = DB()
        return db.get_collection("transcripts").find_one(
            {"video_id": self._video_id}
        )

    def _select_language(self, yt: YouTubeTranscriptApi) -> Optional[Dict]:
        """
        Select a generated transcript language.
        """
        try:
            transcripts = yt.list(self._video_id)

            for t in transcripts:
                if t.is_generated:
                    return {
                        "lan": t.language_code,
                        "translation_lan": [
                            tl.language_code
                            for tl in t.translation_languages
                        ],
                    }

        except Exception as e:
            print(f"[Transcript] Language selection error: {e}")

        return None
    
    def from_generated(self, segments):
        try:
            yt = YouTubeTranscriptApi()
            self._language = self._select_language(yt)

            if not self._language:
                raise NoTranscriptFound("No generated transcript available")
        
            self.segments = segments

            return self.to_dict()

        except Exception as e:
            print(f"Error: {e}")

    def __str__(self) -> str:
        return (
            f"Transcript("
            f"video_id={self._video_id}, "
            f"language={self._language}, "
            f"segments_count={len(self._segments)}"
            f")"
        )