import requests
import json

OLLAMA_URL = "http://localhost:11434/api/chat"

def classify_email(email_content: str) -> str:
    payload = {
        "model": "mistral",
        "messages": [
            {
                "role": "system",
               "content": (
                "You are an email classification assistant. "
                "Your job is to classify an email into one of the following categories:\n"
                "1. Spam - unsolicited or harmful messages.\n"
                "2. Promotion - marketing, advertisements, sales offers.\n"
                "3. Social - personal messages from platforms like LinkedIn, Facebook, Twitter, or invites.\n"
                "4. General - any other normal communication (work, formal, personal, etc.).\n\n"
                "Classify based on the content and subject.\n"
                "Reply with only one word: Spam, Promotion, Social, or General."


                )
            },
            {
                "role": "user",
                "content": email_content.strip()
            }
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()

        # Show raw response for debugging
        raw_text = response.text.strip()

        # Some local LLMs return multiple JSON objects - try to decode only the first line
        try:
            data = json.loads(raw_text)
            category = data.get("message", {}).get("content", "").strip()
            return category
        except json.JSONDecodeError:
            # Fall back to parsing line by line
            for line in raw_text.splitlines():
                try:
                    data = json.loads(line)
                    category = data.get("message", {}).get("content", "").strip()
                    return category
                except json.JSONDecodeError:
                    continue

        return "General"  # fallback if no valid line was found

    except requests.RequestException as e:
        print("Error talking to model:", e)
        return "General"
