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
                "prompt": f"""<|system|>
                    Ты оператор поддержки. Отвечай на русском языке кратко и по делу. 
                    Если вопрос неясен - уточни детали.</s>
                    <|user|>
                    {prompt}</s>
                    <|assistant|>""",
                "stream": False,
                "optoins": {
                    "temperature": 0.3,
                    "top_p": 0.9,
                    "num_ctx": 2048,
                    "repeat_penalty": 1.2,
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
