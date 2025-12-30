from flask import Flask, render_template
from routes.transcript_route import transcript_bp
from routes.video_route import video_bp
from routes.ai_route import ai_bp

app = Flask(__name__)

app.register_blueprint(transcript_bp)
app.register_blueprint(video_bp)
app.register_blueprint(ai_bp)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("/home/home.html")