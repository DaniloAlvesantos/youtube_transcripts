import requests
import json

class AI:
    _default_url = "http://localhost:11434/api"

    def __init__(self, model="llama3.2:1b"):
        self._model = model
        self._url = f"{self._default_url}/generate"
        self._last_summary = None

    def _call_ollama(self, prompt):
        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }
        try:
            response = requests.post(self._url, json=payload)
            response.raise_for_status()
            return response.json().get("response")
        except Exception as e:
            print(f"Ollama Request Error: {e}")
            return None

    def summarize_preaching(self, segments, lang="en"):
        if not segments: return None

        texts = [s.get("text", {}).get(lang, "") for s in segments]
        full_text = " ".join(texts)

        prompt = f"""
        [SYSTEM] You are a theological data analyst.
        [INSTRUCTION]
        1. Identify the core doctrinal points in the transcript.
        2. 'scripture': Extract ONLY the book, chapter, and verse (e.g., "John 21:15-17").
        3. 'quote': Extract the most impactful sentence the preacher said about that point.
        4. If no specific verse is mentioned, use the general Book/Chapter discussed.

        [TRANSCRIPT]
        {full_text}

        [OUTPUT FORMAT]
        {{
            "summary": [
                {{
                    "point": "Basis of ministry",
                    "scripture": "John 21:15",
                    "quote": "The basis of Peter's Ministry would be love"
                }}
            ]
        }}
        """
        
        self._last_summary = self._call_ollama(prompt)
        return self._last_summary

    def generate_dataset(self):
        if not self._last_summary:
            return None

        prompt = f"""
        [SYSTEM] Expert AI Dataset Engineer.
        [CONTEXT] {self._last_summary}
        
        [TASK] Generate 5 instruction-response pairs for a Christian AI.
        [STRUCTURE]
        - prompt: A natural question a user would ask.
        - output: short_answer: [Direct answer] ### exegesis: [Theological depth] ### cross_references: [Other verses] ### application: [Life advice]
        - tags: [Lowercase tags]

        [CONSTRAINT] Use '###' as the exact separator. Return valid JSON.
        """
        
        raw_result = self._call_ollama(prompt)
        
        try:
            return json.loads(raw_result) if isinstance(raw_result, str) else raw_result
        except:
            return None
        
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, model):
        self._model = model