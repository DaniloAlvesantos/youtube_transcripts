# Youtube Transcript

## Techs

- Python
    - flask
    - youtube_transcript_api
    - yt_dlp
    - Threads ( workers )
    - faster-whisper
- MongoDB
- Docker
- Ollama

## Comands

Running application

MAC, LINUX
```cmd
$ source .venv/bin/activate
```

WINDOWS
```cmd
$ ./.venv/Scripts/Activate
```
---

Running Docker
```cmd
$ docker compose up
```

Running Ollama
```cmd
$ ollama run llama3.2:3b
```
Model _llama3.2:3b_ it's for lightweight and testing, for better datasets and summarizes, use a model with more parameters

---

Running mongo shell
```cmd
$ docker exec -it youtube-mongodb mongosh
```

---

## Routes

### /transcript
Route for getting transcript from Youtube api

Features:
- Get transcript from Youtube
- Get saved transcript from Database
- Translate transcript, saved on Database

### /video
Route for transcript a video from Youtube, using whisper

### /ai
Route for summarize a transcript and generate a dataset. The datasets it's for training a model, using fine-tuning