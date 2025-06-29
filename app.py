from flask import Flask, render_template, request
from testmail import call_model
from datetime import datetime
import textwrap

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    output_response = ""
    if request.method == "POST":
        if request.form.get("action") == "generate":
            prompt = request.form["prompt"]
            raw_output = call_model(prompt)
            body = textwrap.fill(raw_output, width=80)
            date = datetime.now().strftime("%B %d, %Y")

            output_response = f"""
Subject: Inquiry

Date: {date}

{body}

Thank you,  
Yours sincerely,  
Name
""".strip()

    return render_template("index.html", output=output_response)

if __name__ == "__main__":
    app.run(debug=True)
