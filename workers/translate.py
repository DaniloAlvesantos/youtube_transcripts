from deep_translator import GoogleTranslator
from models.transcript import Transcript
from models.db import DB

def translate_worker(video_id, target_lang="en"):
    tr = Transcript(video_id)
    data = tr.search_on_db()

    if not data:
        return
    
    segments = data.get("segments", [])
    langs = data.get("languages") or data.get("language")

    if not langs:
        print(f"Erro: Idioma original não encontrado para o vídeo {video_id}")
        return None
    
    if isinstance(langs, list):
        original_lang = langs[0]
    elif isinstance(langs, dict):
        original_lang = langs.get("lan")
    else:
        original_lang = str(langs)

    if isinstance(original_lang, dict): 
        original_lang = original_lang.get("lan")

    texts_to_translate = []
    for s in segments:
        text_dict = s.get("text", {})
        original_text = text_dict.get(original_lang)
        if original_text:
            texts_to_translate.append(original_text)
    
    if not texts_to_translate:
        return segments
    
    try:
        translator = GoogleTranslator(source="auto", target=target_lang)
        translated_texts = translator.translate_batch(texts_to_translate)

        for i, translated_text in enumerate(translated_texts):
            segments[i]["text"][target_lang] = translated_text
        
        db = DB().get_collection("transcripts")
        db.update_one({"video_id": video_id},{
                "$set": {
                    "segments": segments, 
                    "status":"completed"
                },
                "$addToSet": {"languages": target_lang} 
            })
        
    except Exception as e:
        print(f"Erro na tradução: {e}")
        for s in segments:
            s["text"][target_lang] = "[Translation Error]"

    print(f"Translating video {video_id} has done")
    return segments