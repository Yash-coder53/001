import requests
import json
from config import Config

class BlackboxAI:
    def __init__(self):
        self.api_key = Config.BLACKBOX_API_KEY
        self.base_url = "https://www.blackbox.ai/api/chat"
    
    def generate_response(self, message, context=None):
        """Generate response using Blackbox AI"""
        try:
            headers = {
                'Content-Type': 'application/json',
            }
            
            # Prepare the prompt with context
            prompt = f"Previous context: {context}\n\n" if context else ""
            prompt += f"User message: {message}\n\nPlease provide a helpful and engaging response."
            
            payload = {
                "messages": [{"role": "user", "content": prompt}],
                "stream": False
            }
            
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get('response', 'I apologize, but I cannot generate a response at the moment.')
            else:
                return f"Error: API returned status {response.status_code}"
                
        except Exception as e:
            return f"Error generating response: {str(e)}"
