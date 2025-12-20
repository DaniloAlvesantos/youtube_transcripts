from yt_dlp import YoutubeDL
from faster_whisper import WhisperModel
from dtos.transcript_dtos import Transcript_DTOS
import threading
import os

yt_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }
    ],
    "outtmpl": "%(title)s.%(ext)s",
    "quiet": True,
    "restrictfilenames": False, 
}

class YT:
    _default_url = "https://www.youtube.com/watch?v="
    _model = WhisperModel("small", device="cpu", compute_type="int8")

    def __init__(self, video_id: str):
        self._url = f"{self._default_url}{video_id}"

        with YoutubeDL(yt_opts) as ydl:
            info = ydl.extract_info(self._url, download=True)

            self._file_path = info["requested_downloads"][0]["filepath"]

        segments, _ = self._model.transcribe(
            self._file_path,
            vad_filter=True
        )

        transcript = []

        for s in segments:
            d = Transcript_DTOS(s.start, s.end, s.text)

            transcript.append(d.toDict)

        os.remove(self._file_path)

        self._transcript = transcript

    @property
    def transcript(self):
        return self._transcript