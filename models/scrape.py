from requests import get
from bs4 import BeautifulSoup

url = "https://escolabiblicadominical.org/licoes-biblicas-ebd-betel/"
url_config = {
    "contents_selector": {
        "menu": {
            "ul": "ul#menu-primary-items",
            
        }
    }
}

class Scraper:
    pass