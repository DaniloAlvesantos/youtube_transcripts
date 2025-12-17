import requests

class Thumb:
    _api_url = "https://img.youtube.com/vi"
    def __init__(self, video_id):
        self._video_id = video_id
        self._img_url = None

    def extract_thumb(self):
        try:
            response = requests.get(f"{self._api_url}/{self._video_id}/sddefault.jpg")

            if response:
                self._img_url = response.url

                return self._img_url

        except requests.exceptions.RequestException as e:
            print(f"An error ocurred: {e}")
            return ""

    @property
    def img_url(self):
        return self._img_url