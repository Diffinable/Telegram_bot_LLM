import requests
import json
import logging

logging.basicConfig(filename="ollama.log", level=logging.INFO)

def generate_response(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "stream": False,
                "optoins": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "num_ctx": 2048,
                }            
            },
            timeout=30
        )
        response_data = response.json()
        log_generation(prompt, response_data["response"])
        return response_data["response"]
    except Exception as e:
        logging.error(f"Ошибка генерации {e}")
        return "Извините произошла ошибка при генерации запроса"


def log_generation(prompt, response):
    logging.info(f"Prompt: {prompt}\nRepsonse: {response}\n{'='*50}")
