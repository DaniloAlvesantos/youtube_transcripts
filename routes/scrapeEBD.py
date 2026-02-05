from flask import Blueprint, jsonify, request
from models.db import DB
from concurrent.futures import ThreadPoolExecutor
from workers.scrapeEBD import scrapeEBD_process

scrapeEBD_bp = Blueprint("scrape", __name__, url_prefix="/scrape")
executor = ThreadPoolExecutor(max_workers=3)

@scrapeEBD_bp.post("/ebd")
def scrape_ebd():
    data = request.get_json()
    url = data.get("url")
    
    if not url:
        return jsonify(error="URL is required"), 400
    
    db = DB()
    data = db.get_collection("scrapes").find_one({"metadata.source_url": url})
    data["_id"] = str(data["_id"])
    
    if data:
        return jsonify(status="OK", data=data), 200
    
    executor.submit(scrapeEBD_process, url)

    return jsonify(
        status="PROCESSING", 
        message="Scraping started.", 
        url=url
    ), 202

@scrapeEBD_bp.get("/ebd/all")
def scrabeEBD_all():
    db = DB()
    raw_data = db.get_collection("scrapes").find()

    data = []
    for doc in raw_data:
        doc["_id"] = str(doc["_id"])
        data.append(doc)

    return jsonify(
        data=data
    ), 200