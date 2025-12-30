import requests
import json
import math

class AI:
    _default_url = "http://localhost:11434/api"

    def __init__(self, model="llama3.2"):
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
            response = requests.post(self._url, json=payload, timeout=180)
            response.raise_for_status()
            return response.json().get("response")
        except Exception as e:
            print(f"Ollama Request Error: {e}")
            return None

    def summarize_preaching(self, segments, video_id, lang="en"):
        if not segments: return None

        texts = [s.get("text", {}).get(lang, "") for s in segments]
        full_text = " ".join(texts)
        words = full_text.split()
        
        chunk_size = 800
        total_chunks = math.ceil(len(words) / chunk_size)

        all_points = []

        print(f"\n🚀 Starting AI Analysis for {video_id}")
        print(f"📦 Total words: {len(words)} | Chunks to process: {total_chunks}")

        for i in range(total_chunks):
            current_chunk = i + 1

            print(f"⏳ [Chunk {current_chunk}/{total_chunks}] Sending to Llama 3.2 3B...")
            
            start = i * chunk_size
            end = start + chunk_size
            chunk_text = " ".join(words[start:end])

            prompt = f"""
            [SYSTEM] You are a Theological Content Filter.
            [INSTRUCTION]
            1. EXTRACT only theological and doctrinal insights from the transcript.
            2. IGNORE all procedural, administrative, and contact information. 
            3. DO NOT include: phone numbers, websites, physical addresses, instructions on how to call counselors, or appeals for donations.
            4. If a point is purely a "Call to Action" for a phone line, DISCARD it.
            5. Strictly use the provided text; do not add external biblical knowledge.

            [TRANSCRIPT]
            {chunk_text}

            [OUTPUT FORMAT]
            {{
                "summary": [
                    {{
                        "point": "Doctrinal point name",
                        "scripture": "Book Chapter:Verse",
                        "quote": "Sermon excerpt"
                    }}
                ]
            }}
            """
            
            result = self._call_ollama(prompt)
            
            try:
                data = json.loads(result)
                if "summary" in data:
                    all_points.extend(data["summary"])
                    print(f"✅ [Chunk {current_chunk}/{total_chunks}] Success! Extracted {len(data['summary'])} points.")
            except Exception as e:
                print(f"❌ [Chunk {current_chunk}/{total_chunks}] Failed to parse JSON: {e}")

        self._last_summary = {"summary": all_points}
        return self._last_summary

    def generate_dataset(self):
        if not self._last_summary:
            return None

        prompt = f"""
        [SYSTEM] Expert AI Dataset Engineer for Christian Instruction.
        [CONTEXT] {self._last_summary}

        [TASK] Generate 5 instruction-response pairs for a theological assistant.
        [STRICT RULES]
        - All prompts and outputs must be SPIRITUAL or DOCTRINAL.
        - Never mention contact info, television schedules, or phone numbers in the dataset.
        - Focus on the 'Exegesis' and 'Application' of the Word of God.
        - Ensure the 'prompt' sounds like a question from a believer seeking guidance.

        [STRUCTURE]
        prompt: ... ### output: short_answer: ... ### exegesis: ... ### cross_references: ... ### application: ...
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