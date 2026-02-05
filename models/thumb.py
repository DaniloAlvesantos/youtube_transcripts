import requests
from utils.logging_helper import log_error

class Thumb:
    """
    EXTRACT THUMBNAILS FROM 
    YOUTUBE VIDEOS
    """
    
    _api_url: str = "https://img.youtube.com/vi"
    def __init__(self, video_id: str):
        self._video_id:str = video_id
        self._img_url = None

    def extract_thumb(self) -> (str | None):
        try:
            response = requests.get(f"{self._api_url}/{self._video_id}/sddefault.jpg")

            if response:
                self._img_url = response.url

                return self._img_url

        except requests.exceptions.RequestException as e:
            log_error(f"An error ocurred: {e}")
            return ""

    @property
    def img_url(self) -> (str | None):
        return self._img_url