
📧 Email Assistant with LLM and Gmail Integration

🔧 Features

- ✍️ Generate professional emails using prompts.
- 🚫 Detect spam using a local AI model (Mistral via Ollama).
- 📥 Manage a local inbox with spam filtering, starring, and categorization (General, Promotion, Social).
- 💌 View full email content with a "Go Back" option.
- 📬 Fetch real Gmail inbox content using the Gmail API.
- 🖱️ Copy content, format fonts, and delete emails easily.
- 🗃️ Emails are stored locally in JSON (inbox_data.json).

⚙️ Setup Instructions

1. 📥 Install Ollama

Download and install Ollama from the official website:
👉 https://ollama.com

Ollama runs a local server that serves open-source LLMs like Mistral.

2. 🧠 Download and Run Mistral Model via Ollama

    ollama run mistral

Ensure Ollama is running at http://localhost:11434.

3. 💻 Clone This Repository

    git clone https://github.com/ptpnaji123/Email_Generation_LLM.git
    cd Email_Generation_LLM

4. 🐍 Set Up Python Environment

Ensure Python 3.8+ is installed.

    python -m venv venv
    source venv/bin/activate      # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

If requirements.txt is missing, install manually:

    pip install Flask google-api-python-client google-auth google-auth-oauthlib

5. 📧 Setup Gmail API

To fetch real emails from Gmail:

a. Go to Google Cloud Console:
👉 https://console.cloud.google.com

- Create a project (or use an existing one)
- Go to APIs & Services > Library
- Search for Gmail API and enable it

b. Set Up OAuth 2.0 Credentials

- Go to APIs & Services > Credentials
- Click Create Credentials > OAuth client ID
- Choose Desktop App
- Download the generated file and rename it:

    credentials.json

Place this credentials.json file in the root directory of your project.

c. Generate token.json

The first time you run Gmail integration, a browser window will open asking for permission. After allowing access, token.json will be created automatically in the same directory. This stores your access tokens securely.

6. ▶️ Run the Flask App

    python app.py

Then visit in your browser:

    http://localhost:5000


✅ Usage Instructions

- Generate Email: Enter a prompt and receive a formal email.
- Detect Spam Email: Paste any text and detect if it’s spam.
- Inbox:
  - Switch views between General, Promotion, Social, and Spam.
  - Click email to view full content and go back using “Go Back” button.
  - Star important emails.
- Fetch Gmail:
  - Click “Fetch Gmail” button to load your real Gmail inbox into the app.

🧠 Model & Prompting Logic

All LLM requests are sent to:
http://localhost:11434/api/chat

Using Mistral via Ollama.

Email Generation Prompt:
"You are a helpful assistant that writes professional emails."

Spam Detection Prompt:
"You are a spam detection AI. Respond with only 'Spam' or 'Not Spam' based on the email content."

📌 Notes

- Email rendering uses HTML safely with proper formatting.
- Gmail fetching requires one-time verification to create token.json.
- All emails are categorized for better filtering and stored locally.
