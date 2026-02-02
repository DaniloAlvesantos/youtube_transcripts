from flask import Flask
from routes.transcript_route import transcript_bp
from routes.video_route import video_bp
from routes.ai_route import ai_bp
from routes.scrapeEBD import scrapeEBD_bp
from models.db import DB

app = Flask(__name__)

app.register_blueprint(transcript_bp)
app.register_blueprint(video_bp)
app.register_blueprint(ai_bp)
app.register_blueprint(scrapeEBD_bp)

@app.route("/db", methods=["GET"])
def health_db():
    db = DB()
    try:
        db.client.admin.command('ping')
        return {"status": "Database connection is healthy."}, 200
    except Exception as e:
        return {"status": "Database connection failed.", "error": str(e)}, 500

if __name__ == "__main__":
    app.run(debug=True)