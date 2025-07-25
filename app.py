from flask import Flask, render_template, request, redirect, url_for, jsonify
from testmail import call_model
from classify_email import classify_email
from storage import save_mail, get_all_emails, get_email_by_id, delete_emails_by_ids
from datetime import datetime
from gmailfetcher import authenticate_gmail, fetch_emails

app = Flask(__name__)

@app.route("/fetch_gmail")
def fetch_gmail():
    service = authenticate_gmail()
    emails = fetch_emails(service, max_results=5)

    for email in emails:
        category = classify_email(email['body'])
        is_spam = (category.lower() == "spam")
        save_mail({
            "subject": email["subject"],
            "from": email["from"],
            "date": datetime.now().strftime("%B %d, %Y"),
            "body": email["body"],
            "paragraphs": [],
            "sub_category": category,
            "starred": False,
            "read": False
        }, is_spam=is_spam)

    return redirect(url_for("inbox"))

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
            content = " ".join(result.get("paragraphs", []))
            result["sub_category"] = classify_email(content)
            result["starred"] = False
            result["read"] = False
            email_data = result  # No saving to storage
        else:
            email_data = {"error": result["error"]}

    return render_template("index.html", email=email_data)

@app.route("/spam", methods=["GET", "POST"])
def spam():
    result = None
    if request.method == "POST":
        content = request.form["email_content"]
        category = classify_email(content)
        is_spam = (category.lower() == "spam")

        email_data = {
            "subject": content[:80] + "..." if len(content) > 80 else content,
            "body": content.strip(),
            "paragraphs": [],
            "date": datetime.now().strftime("%B %d, %Y"),
            "sub_category": category,
            "starred": False,
            "read": False
        }

        save_mail(email_data, is_spam=is_spam)
        result = category

    return render_template("spam.html", result=result)

@app.route("/inbox")
def inbox():
    filter_main = request.args.get("filter", "mail")
    sub_filter = request.args.get("sub", "general")

    if filter_main == "spam":
        emails = get_all_emails("spam", "spam")
        heading = "🚫 Spam Mails"
        category = "spam"
    elif filter_main == "starred":
        emails = [e for e in get_all_emails("mail", "all") + get_all_emails("spam", "all") if e.get("starred")]
        heading = "⭐ Starred Mails"
        category = "starred"
    else:
        emails = get_all_emails("mail", sub_filter)
        heading = {
            "promotion": "📢 Promotion Mails",
            "social": "👥 Social Mails",
            "general": "📧 All Mails"
        }.get(sub_filter.lower(), "📧 All Mails")
        category = "mail"

    return render_template("inbox.html", emails=emails, heading=heading, category=category, sub_filter=sub_filter)

@app.route("/inbox/<category>/<int:email_id>")
def view_email(category, email_id):
    sub_filter = request.args.get("sub") or ("spam" if category == "spam" else "general")
    if category == "spam":
        sub_filter = "spam"

    if category == "starred":
        # Look into both mail and spam for starred
        emails = [e for e in get_all_emails("mail", "all") + get_all_emails("spam", "all") if e.get("starred")]
    else:
        emails = get_all_emails(category, sub_filter)

    if 0 <= email_id < len(emails):
        email = emails[email_id]
        if not email.get("read", False) and category != "starred":
            email["read"] = True
            all_emails = get_all_emails(category, sub_filter)
            all_emails[email_id] = email
            from storage import _load_data, _save_data
            data = _load_data()
            data[category][sub_filter] = all_emails
            _save_data(data)
        return render_template("view_email.html", email=email)
    return "Email not found", 404

@app.route("/delete", methods=["POST"])
def delete_emails():
    category = request.form.get("category")
    sub_filter = request.form.get("sub") or "general"

    selected_ids = [int(i) for i in request.form.getlist("selected")]
    if category in ("mail", "spam") and selected_ids:
        delete_emails_by_ids(category, selected_ids, sub_filter)

    redirect_filter = "spam" if category == "spam" else None
    return redirect(url_for("inbox", filter=redirect_filter, sub=sub_filter))

@app.route("/toggle_star/<category>/<int:email_id>", methods=["POST"])
def toggle_star(category, email_id):
    sub_filter = request.args.get("sub") or ("spam" if category == "spam" else "general")
    email = get_email_by_id(category, email_id, sub_filter)
    if not email:
        return jsonify({"error": "Email not found"}), 404

    email["starred"] = not email.get("starred", False)
    all_emails = get_all_emails(category, sub_filter)
    all_emails[email_id] = email
    from storage import _load_data, _save_data
    data = _load_data()
    data[category][sub_filter] = all_emails
    _save_data(data)

    return jsonify({"starred": email["starred"]})

if __name__ == "__main__":
    app.run(debug=True)
