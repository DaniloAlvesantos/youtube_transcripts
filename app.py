from flask import Flask, render_template
from routes.transcript_route import transcript_bp
from routes.video_route import video_bp

app = Flask(__name__)

app.register_blueprint(transcript_bp)
app.register_blueprint(video_bp)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("/home/home.html")

"""
Install pip install googletrans

for translating the transcript.
"""