import requests

class Engine:
    api_key: str
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Please provide an API key")
        self.api_key = api_key
        self._base_url = "https://api.rsnai.org/api/v1/user/"

    def _make_request(self, endpoint: str, prompt: str):
        url = f"{self._base_url}{endpoint}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        payload = {"prompt": prompt}
        
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            error_message = response.json().get("error", {}).get("message", str(e))
            raise ValueError(f"Request failed: {error_message}")

    def gpt(self, prompt: str):
        return self._make_request("gpt", prompt)

    def prodia(self, prompt: str):
        return self._make_request("prodia", prompt)
    
engine=Engine("rsnai_7jE3tAy2EJl7bhl4iyYNcdjZ")
    
class Neurum:
    token: str
    def generate(self, prompt: str):
        response = engine.gpt(prompt)
        message = response.get('message', '')
        return message
    def chat(messages: list[dict]):
        response = engine.gpt(messages[-1]['content'])
        message = response.get('message', '')
        return message