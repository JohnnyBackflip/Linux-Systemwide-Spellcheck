import requests
import json

class GeminiClient:
    def __init__(self, config_manager):
        self.config = config_manager
        self.base_url = "https://generativelanguage.googleapis.com/v1beta"

    def get_models(self):
        api_key = self.config.get("api_key")
        if not api_key:
            return ["gemini-3.1-flash-lite-preview"]
        
        url = f"{self.base_url}/models?key={api_key}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = []
                for model in data.get("models", []):
                    # Check if model supports generateContent
                    if "generateContent" in model.get("supportedGenerationMethods", []):
                        name = model.get("name", "").replace("models/", "")
                        display_name = model.get("displayName", "")
                        
                        # Exclusions
                        combined_name = (name + " " + display_name).lower()
                        if "banana" in combined_name or "robotics" in combined_name or "research" in combined_name:
                            continue
                        
                        models.append(name)
                
                # Force fallback model if not present
                if "gemini-3.1-flash-lite-preview" not in models:
                    models.insert(0, "gemini-3.1-flash-lite-preview")
                return models
        except Exception as e:
            print(f"Error fetching models: {e}")
        
        return ["gemini-3.1-flash-lite-preview"]

    def correct_text(self, text):
        api_key = self.config.get("api_key")
        if not api_key:
            return "Error: API Key is missing. Please set it in Settings."

        model = self.config.get("model", "gemini-3.1-flash-lite-preview")
        system_prompt = self.config.get("system_prompt", "Correct the spelling and grammar of the following text. Only return the corrected text, no conversational filler or explanation.")
        
        url = f"{self.base_url}/models/{model}:generateContent?key={api_key}"
        
        headers = {"Content-Type": "application/json"}
        
        payload = {
            "systemInstruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [
                {
                    "parts": [{"text": text}]
                }
            ],
            "safetySettings": [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE"
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE"
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=20)
            if response.status_code == 200:
                data = response.json()
                try:
                    corrected = data['candidates'][0]['content']['parts'][0]['text']
                    return corrected.strip()
                except KeyError:
                    return f"Error: Unexpected API response structure.\n{data}"
            else:
                return f"API Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: Failed to connect to API.\n{str(e)}"
