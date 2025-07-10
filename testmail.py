import requests
import re

OLLAMA_URL = "http://localhost:11434/api/chat"

def call_model(prompt: str) -> dict:
    payload = {
        "model": "mistral",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant that writes professional emails."},
            {"role": "user", "content": prompt.strip()}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        content = response.json()["message"]["content"].strip()
        return parse_email(content)
    except requests.RequestException as e:
        return {"error": f"Error communicating with Ollama: {e}"}

def parse_email(raw_email: str) -> dict:
    subject_match = re.search(r"(Subject:.*?)\n", raw_email, re.IGNORECASE)
    greeting_match = re.search(r"(Dear .*?,)", raw_email)
    closing_match = re.search(r"(Best regards,.*)", raw_email, re.DOTALL | re.IGNORECASE)

    subject = subject_match.group(1).strip() if subject_match else "Subject: [No subject found]"
    greeting = greeting_match.group(1).strip() if greeting_match else "Dear Sir/Madam,"
    closing = closing_match.group(1).strip() if closing_match else "Best regards,\nName"

    body = raw_email
    for part in [subject, greeting, closing]:
        body = body.replace(part, '')

    paragraphs = [p.strip() for p in body.strip().split('\n') if p.strip()]
    return {
        "subject": subject,
        "greeting": greeting,
        "paragraphs": paragraphs,
        "closing": closing
    }
