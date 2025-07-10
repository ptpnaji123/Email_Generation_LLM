import requests

OLLAMA_URL = "http://localhost:11434/api/chat"

def detect_spam(email_content: str) -> str:
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "system", "content": "You are a spam detection AI. Respond with only 'Spam' or 'Not Spam' based on the email content."},
            {"role": "user", "content": email_content.strip()}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        prediction = response.json()["message"]["content"].strip()
        return prediction
    except requests.RequestException as e:
        return f"Error: {e}"
