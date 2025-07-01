import torch
from transformers import pipeline

class TinyLlameChat:
    def __init__(self):
        self.pipe = pipeline(
            "text-generation",
            model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
            torch_dtype=torch.bfloat16,
            device_map="auto",  
        )

    def generate_response(self, user_message):
        messages = [
            {
                "role": "system",
                "content": "Вы помошник службы поддержки. Отвечайте вежливо и по делу.",
            },
            {
                "role": "user", "content": user_message,
            },
        ]
        prompt = self.pipe.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )


        outputs = self.pipe(
            prompt,
            max_new_tokens=200,
            do_sample=True,
            temperature=0.7,
            top_k=50,
            top_p=0.95,
            repetition_penalty=1.1,
        )
        full_response = outputs[0]["generated_text"]
        return full_response.split("<|assistant|>")[-1].strip()
    
if __name__ == "__main__":
    llm = TinyLlameChat()
    response = llm.generate_response("Как похудеть к лету")
    print(f"Ответ: {response}")
    