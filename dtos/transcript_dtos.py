class Transcript_DTOS:
    start: float
    end: float
    text:str

    def __init__(self, start:float, end:float, text: str):
        self.start = start
        self.end = end
        self.text = text

    @property
    def toDict(self):
        return {
            "start": self.start,
            "end": self.end,
            "text": self.text
        }