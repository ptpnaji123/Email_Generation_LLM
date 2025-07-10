# 📧 Email Generation and Spam Detection using LLM (Mistral + Ollama)

This project is a Flask-based web application that allows users to:
- Generate professional emails using the Mistral LLM via Ollama.
- Detect whether pasted email content is **spam** or **not spam**.
- View, manage, and delete stored emails (spam and non-spam) with a clean UI.

---

## 🔧 Features

- ✍️ Email generation using prompts.
- 🚫 Spam detection for custom email content.
- 📨 Mail inbox and spam section with viewing and deleting.
- 🎨 Interactive front-end with font formatting and copy options.
- ✅ Mails stored locally in `inbox_data.json`.

---

## ⚙️ Setup Instructions

### 1. 📥 Install Ollama

Download and install Ollama from their official website:

👉 https://ollama.com

> Ollama runs a local server to interface with open-source large language models.

---

### 2. 🚀 Run Ollama and Download the Mistral Model

Open your terminal and start Ollama:

```bash
ollama run mistral
```
### 3. 💻 Clone This Repository

```bash
git clone https://github.com/ptpnaji123/Email_Generation_LLM.git
cd Email_Generation_LLM
```

---

### 4. 🐍 Set Up Python Environment

Ensure Python 3.8+ is installed.

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> If `requirements.txt` does not exist, manually install Flask:
```bash
pip install Flask
```

---

### 5. ▶️ Run the Flask App

```bash
python app.py
```

Navigate to `http://localhost:5000` in your browser.

---

## 📁 Project Structure

```
Email_Generation_LLM/
│
├── app.py                  # Main Flask app
├── testmail.py             # Calls Mistral model via Ollama
├── spam_model.py           # Detects spam using Mistral
├── storage.py              # Handles email storage and retrieval
├── inbox_data.json         # Stores all emails
│
├── templates/              # HTML files
│   ├── home.html
│   ├── inbox.html
│   ├── index.html
│   ├── spam.html
│   └── view_email.html
│
├── static/
│   └── styles.css          # Styling
│
├── .gitignore              # (optional) Ignore cache or sensitive files
└── README.md
```

---

## ✅ Usage Instructions

- Click **"Generate Email"** to enter a prompt and get a professional email.
- Click **"Detect Spam Email"** to test whether content is spam.
- Use the **Inbox sidebar** to browse spam or non-spam emails.
- Use **checkboxes** to select and delete specific emails.

---

## 🧠 Model & Prompting Logic

- All LLM requests are sent to `http://localhost:11434/api/chat` using Mistral.
- Email generation prompt uses:
  ```python
  "You are a helpful assistant that writes professional emails."
  ```
- Spam detection prompt uses:
  ```python
  "You are a spam detection AI. Respond with only 'Spam' or 'Not Spam' based on the email content."
  ```


## 📜 License

This project is for educational/demo purposes. Adapt as needed for production use.
