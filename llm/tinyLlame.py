from transformers import AutoTokenizer, AutoModelForCausalLM

class TinyLlame:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
        self.model = AutoModelForCausalLM.from_pretrained("TinyLlama/TinyLlama-1.1B-Chat-v1.0")

    def generate_response(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_new_tokens=100)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response
    
if __name__ == "__main__":
    llm = TinyLlame()
    response = llm.generate_response("Привет, как дела?")
    print(response)