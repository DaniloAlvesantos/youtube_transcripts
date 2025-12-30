from yt_dlp import YoutubeDL
from faster_whisper import WhisperModel
from dtos.transcript_dtos import Transcript_DTOS
from models.db import DB
import os

yt_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }
    ],
    "quiet": True,
    "restrictfilenames": True, 
}

class YT:
    _default_url = "https://www.youtube.com/watch?v="
    _model = WhisperModel("small", device="cpu", compute_type="int8")

    def __init__(self, video_id: str):
        self._video_id = video_id
        self._url = f"{self._default_url}{video_id}"
        self._detected_language = None
        self._transcript = []
        self._process()

    def _process(self):
        current_opts = yt_opts.copy()
        current_opts["outtmpl"] = f"{self._video_id}.%(ext)s"
        db = DB().get_collection("transcripts")

        try:
            with YoutubeDL(current_opts) as ydl:
                info = ydl.extract_info(self._url, download=True)
                file_path = info["requested_downloads"][0]["filepath"]

            db.update_one({"video_id": self._video_id}, {"$set": {"status": "transcribing"}})
            segments, info = self._model.transcribe(
                file_path,
                vad_filter=True
            )

            self._detected_language = info.language
            
            formatted_transcript = []
            for s in segments:
                d = Transcript_DTOS(s.start, s.end, s.text)
                formatted_transcript.append(d.toDict)

            self._transcript = formatted_transcript

            if os.path.exists(file_path):
                os.remove(file_path)
                
        except Exception as e:
            raise e

    @property
    def transcript(self):
        return self._transcript

    @property
    def detected_language(self):
        return self._detected_language

    @property
    def video_id(self):
        return self._video_id