from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Replace with the exact model name for Llama 3 8B once available
model_name = "meta-llama/Llama-3-8b-chat-hf"  # Example model name
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_summary(text, max_length=150):
    """Generate a summary for the given text using Llama 3 8B."""
    inputs = tokenizer(text, return_tensors="pt").input_ids
    outputs = model.generate(inputs, max_length=max_length, num_beams=5, early_stopping=True)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
