from datetime import datetime
from models.scrapeEBD import ScrapeEBD
from models.db import DB

def scrapeEBD_process(url):
    db = DB().get_collection("scrapes")
    query = {"metadata.source_url": url}
    
    try:
        db.update_one(
            query,
            {
                "$set": {
                    "status": "downloading",
                    "metadata.source_url": url,
                    "metadata.ingested_at": datetime.now().isoformat() + "Z"
                }
            }, 
            upsert=True
        )
        
        scrape = ScrapeEBD(url)
        content, raw_content, html, title = scrape.scrate_target_html()

        if not content:
            raise Exception("O conteúdo retornado pelo Docling está vazio.")
        
        db.update_one(
            query,
            {
                "$set": {
                    "status": "completed",
                    "metadata.title": f"{title}", 
                    "content.full_markdown": content,
                    "content.raw_html_snippet": str(html)
                }
            }
        )
        return content

    except Exception as e:
        db.update_one(
            query,
            {
                "$set": {
                    "status": "error",
                    "error_msg": str(e),
                    "error_at": datetime.utcnow().isoformat()
                }
            }
        )
        
        print(f"❌ Erro na URL {url}: {e}")
        
        return None