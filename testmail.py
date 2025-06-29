import torch
from transformers import pipeline

# Load model once
model_tag = "pszemraj/opt-350m-email-generation"
device = 0 if torch.cuda.is_available() else -1

email_gen = pipeline(
    "text-generation",
    model=model_tag,
    use_fast=False,
    device=device
)

def call_model(
    prompt: str,
    max_new_tokens: int = 50,
    num_beams: int = 4,
    temperature: float = 0.3,
    no_repeat_ngram_size: int = 3,
    repetition_penalty: float = 3.5,
    length_penalty: float = 0.8,
) -> str:
    result = email_gen(
        prompt.strip(),
        max_new_tokens=max_new_tokens,  # Limit to 100 new tokens
        no_repeat_ngram_size=no_repeat_ngram_size,
        repetition_penalty=repetition_penalty,
        length_penalty=length_penalty,
        temperature=temperature,
        do_sample=False,
        num_beams=num_beams,
        return_full_text=True  # Don't include the original prompt in the output
    )

    response = result[0]["generated_text"].strip()

    # Optional: free GPU memory
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return response


# --- Additions Below --- #

def get_model_info():
    """Returns basic information about the loaded model."""
    return {
        "model_tag": model_tag,
        "device": "cuda" if torch.cuda.is_available() else "cpu"
    }


def extract_clean_body(full_text: str, prompt: str) -> str:
    """Removes the prompt from full text and returns only the model's response."""
    return full_text.replace(prompt.strip(), "").strip()


if __name__ == "__main__":
    print("=== Quick Email Prompt Test ===")
    while True:
        prompt = input("Enter your prompt (or type 'exit'): ")
        if prompt.lower().strip() == "exit":
            break
        output = call_model(prompt)
        print("\n--- Generated Email ---\n")
        print(output)
        print("\n")
