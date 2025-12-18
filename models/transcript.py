import os
import json
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoUnavailable
from .thumb import Thumb


class Transcript:
    def __init__(self, video_id):
        self._video_id = video_id
        self._language = None
        self._segments = []
        self._thumb = None
    
    def fetch_transcription(self):
        self._segments = []

        try: 
            yt = YouTubeTranscriptApi()
            self._language = self.list_transcripts(yt=yt)
            print("lang:20", self._language)

            if not self._language:
                raise NoTranscriptFound("No generated transcript available")

            yt_response = yt.fetch(self._video_id, languages=[self._language["lan"]])

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
    
    def list_transcripts(self, yt: YouTubeTranscriptApi):
        if not self._video_id:
            return {}

        try:
            t_list = yt.list(self._video_id)
            t_available = None

            for t in t_list:
                if t.is_generated:
                    t_available = {
                        "lan": t.language_code,
                        "translation_lan": [
                            tl.language_code for tl in t.translation_languages
                        ]
                    }

                print(
                    t.video_id,
                    t.language,
                    t.language_code,
                    t.is_generated,
                    t.translation_languages
                )

            return t_available

        except Exception as e:
            print(f"Erro ao listar: {e}")
            return {}


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