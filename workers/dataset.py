from models.ai import AI
from models.db import DB

def process_dataset(segments, lang, video_id):
    ai = AI()
    summ = ai.summarize_preaching(segments, lang)
    print("summarize: ", summ)
    print()
    dataset = ai.generate_dataset()
    print("datasets: ", dataset)
    print()
    db = DB()
    collection = db.get_collection("datasets")

    collection.update_one(
            {"_id": video_id},
            {"$set": {
                "datasets": dataset,
            }},
            upsert=True
        )
    