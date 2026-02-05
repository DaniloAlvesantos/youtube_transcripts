import requests
from bs4 import Tag
from io import BytesIO
from bs4 import BeautifulSoup
from docling.document_converter import DocumentConverter
from docling.datamodel.base_models import DocumentStream
from utils.logging_helper import log_error

class ScrapeEBD:
    def __init__(self, url: str):
        self._url:str = url
        self._converter: DocumentConverter = DocumentConverter()

    def scrate_target_html(self, target_tag: str="article") -> (tuple[str, str, Tag, str] | None):
        try:
            response = requests.get(self._url)
            soup = BeautifulSoup(response.text, "html.parser")
            target_element = soup.find(target_tag)
            title = soup.title.string or "-"

            if not target_element:
                log_error(f"⚠️ Tag <{target_tag}> não encontrada.")
                return None

            html_content = str(target_element).encode("utf-8")
                        
            raw_source = DocumentStream(
                name="snippet.html", 
                stream=BytesIO(html_content)
            )

            result = self._converter.convert(raw_source)
            raw = result.document.export_to_markdown()
            
            clean_html = self.clean_html(target_element)
            clean_source = DocumentStream(
                name="snippet.html", 
                stream=BytesIO(clean_html.encode("utf-8"))
            )
            
            output = self._converter.convert(clean_source).document.export_to_markdown()
            
            return output, raw, target_element, title

        except Exception as e:
            log_error(f"❌ Erro ao converter: {e}")
            

    def clean_html(self, soup: Tag) -> str:
        trash_selectors = [
            "header", "footer", "nav", "aside", ".sidebar", ".comments",
            ".ads", ".social-share", "script", "style", "noscript", 
            ".related-posts", ".menu", "meta",
            "p:contains('Pix:')", 
        ]
    
        for selector in trash_selectors:
            for element in soup.select(selector):
                element.decompose()
            
        return str(soup).strip()
    
    def __str__(self):
        return f"ScrapeEBD(url={self._url})"
    
    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, url: str) -> str:
        self._url = url
        return self._url