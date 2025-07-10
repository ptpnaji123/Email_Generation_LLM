import json
import os

STORAGE_FILE = "inbox_data.json"

# Initialize structure
if not os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "w") as f:
        json.dump({"mail": [], "spam": []}, f)


def _load_data():
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)


def _save_data(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)


def save_mail(email_data: dict, is_spam=False):
    data = _load_data()
    category = "spam" if is_spam else "mail"
    data[category].append(email_data)
    _save_data(data)


def get_all_emails(category: str):
    data = _load_data()
    return data.get(category, [])


def get_email_by_id(category: str, email_id: int):
    emails = get_all_emails(category)
    try:
        return emails[email_id]
    except IndexError:
        return None


def delete_emails_by_ids(category: str, ids: list):
    data = _load_data()
    if category not in data:
        return

    # Safely remove by index (highest to lowest to avoid shift)
    for idx in sorted(ids, reverse=True):
        try:
            del data[category][idx]
        except IndexError:
            continue

    _save_data(data)