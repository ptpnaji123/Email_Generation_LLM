from flask import Flask, render_template, request, redirect, url_for, jsonify
from testmail import call_model
from classify_email import classify_email
from storage import save_mail, get_all_emails, get_email_by_id, delete_emails_by_ids
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
            content = " ".join(result.get("paragraphs", []))
            category = classify_email(content)
            result["sub_category"] = category
            result["starred"] = False  # Default starred status
            is_spam = category.lower() == "spam"
            save_mail(result, is_spam=is_spam)
            email_data = result
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
            "date": datetime.now().strftime("%B %d, %Y"),
            "sub_category": category,
            "starred": False  # Default starred status
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
        all_mails = get_all_emails("mail", "all")
        all_spams = get_all_emails("spam", "all")
        emails = [e for e in all_mails + all_spams if e.get("starred", False)]
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
    sub_filter = request.args.get("sub", "spam" if category == "spam" else "general")
    email = get_email_by_id(category, email_id, sub_filter)
    if not email:
        return "Email not found", 404
    return render_template("view_email.html", email=email)

@app.route("/delete", methods=["POST"])
def delete_emails():
    category = request.form.get("category")
    sub_filter = request.form.get("sub")

    # Ensure sub_filter is correct
    if not sub_filter or category == "spam":
        sub_filter = "spam" if category == "spam" else "general"

    selected = request.form.getlist("selected")
    selected_ids = [int(idx) for idx in selected]

    if category in ("mail", "spam") and selected_ids:
        delete_emails_by_ids(category, selected_ids, sub_filter)

    redirect_filter = "spam" if category == "spam" else None
    return redirect(url_for("inbox", filter=redirect_filter, sub=sub_filter))



@app.route("/toggle_star/<category>/<int:email_id>", methods=["POST"])
def toggle_star(category, email_id):
    sub_filter = request.args.get("sub")

    if not sub_filter:
        sub_filter = "spam" if category == "spam" else "general"

    if category == "spam":
        sub_filter = "spam"  # Force it for spam mails

    email = get_email_by_id(category, email_id, sub_filter)
    if not email:
        return jsonify({"error": "Email not found"}), 404

    email["starred"] = not email.get("starred", False)

    all_emails = get_all_emails(category, sub_filter)
    if 0 <= email_id < len(all_emails):
        all_emails[email_id] = email
        from storage import _load_data, _save_data
        store = _load_data()
        store[category][sub_filter] = all_emails
        _save_data(store)

    return jsonify({"starred": email["starred"]})

if __name__ == "__main__":
    app.run(debug=True)
