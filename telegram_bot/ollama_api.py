import os
import requests
import json
import logging

logging.basicConfig(filename="ollama.log", level=logging.INFO)
OLLAMA_HOST = os.getenv("OLLAMA_HOST")


def generate_response(prompt: str) -> str:
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": "mistral",
                "prompt": f"""<|system|>
                    Ты русскоязычный ассистент. Отвечай кратко и точно. 
                    </s>
                    <|user|>
                    {prompt}</s>
                    <|assistant|>""",
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "top_p": 0.9,
                    "num_ctx": 1024,
                    "repeat_penalty": 1.2,
                }            
            },
            timeout=120
        )
        response_data = response.json()
        log_generation(prompt, response_data["response"])
        return response_data["response"]
    except Exception as e:
        logging.error(f"Ошибка генерации {e}")
        return "Извините произошла ошибка при генерации запроса"


def log_generation(prompt, response):
    logging.info(f"Prompt: {prompt}\nRepsonse: {response}\n{'='*50}")
