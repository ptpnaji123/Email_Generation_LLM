from flask import Flask, render_template, request, redirect, url_for
from testmail import call_model
from spam_model import detect_spam
from storage import save_mail, get_all_emails, get_email_by_id
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/generate", methods=["GET", "POST"])
def generate():
    email_data = {}

    if request.method == "POST":
        prompt = request.form["prompt"]
        result = call_model(prompt)
        if "error" not in result:
            result["date"] = datetime.now().strftime("%B %d, %Y")
            email_data = result
            save_mail(email_data, is_spam=False)
        else:
            email_data = {"error": result["error"]}

    return render_template("index.html", email=email_data)

@app.route("/spam", methods=["GET", "POST"])
def spam():
    result = None
    if request.method == "POST":
        content = request.form["email_content"]
        prediction = detect_spam(content)
        result = prediction

        email_data = {
            "subject": f"Spam Check Result - {datetime.now().strftime('%B %d, %Y')}",
            "body": content.strip(),
            "date": datetime.now().strftime("%B %d, %Y")
        }

        is_spam = prediction.lower() == "spam"
        save_mail(email_data, is_spam=is_spam)

    return render_template("spam.html", result=result)
@app.route("/inbox")
def inbox():
    filter_type = request.args.get("filter", "all")

    if filter_type == "spam":
        emails = get_all_emails("spam")
        heading = "🚫 Spam Mails"
        category = "spam"
    else:
        emails = get_all_emails("mail")
        heading = "📧 All Mails"
        category = "mail"

    return render_template("inbox.html", emails=emails, heading=heading, category=category)


@app.route("/inbox/<category>/<int:email_id>")
def view_email(category, email_id):
    email = get_email_by_id(category, email_id)
    if not email:
        return "Email not found", 404
    return render_template("view_email.html", email=email)


@app.route("/delete", methods=["POST"])
def delete_emails():
    category = request.form.get("category")
    selected = request.form.getlist("selected")
    selected_ids = [int(idx) for idx in selected]
    
    if category in ("mail", "spam") and selected_ids:
        from storage import delete_emails_by_ids
        delete_emails_by_ids(category, selected_ids)

    return redirect(url_for("inbox", filter=category if category == "spam" else None))



if __name__ == "__main__":
    app.run(debug=True)
