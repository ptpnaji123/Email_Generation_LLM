import json
import os
from typing import List, Optional

STORAGE_FILE = "inbox_data.json"

# Initialize structure
if not os.path.exists(STORAGE_FILE):
    with open(STORAGE_FILE, "w") as f:
        json.dump({
            "mail": {
                "general": [],
                "promotion": [],
                "social": []
            },
            "spam": {
                "spam": []
            }
        }, f, indent=4)

def _load_data() -> dict:
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def _save_data(data: dict):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_mail(email_data: dict, is_spam: bool = False):
    data = _load_data()
    main_category = "spam" if is_spam else "mail"
    sub_category = email_data.get("sub_category", "general").lower()

    if main_category == "spam":
        sub_category = "spam"
    elif sub_category not in ["promotion", "social"]:
        sub_category = "general"

    data.setdefault(main_category, {}).setdefault(sub_category, []).append(email_data)
    _save_data(data)

def get_all_emails(category: str, sub: str = "general") -> List[dict]:
    data = _load_data()
    category_data = data.get(category, {})

    if sub == "all":
        all_emails = []
        for emails in category_data.values():
            all_emails.extend(emails)
        return all_emails

    return category_data.get(sub, [])

def get_email_by_id(category: str, email_id: int, sub: str = "general") -> Optional[dict]:
    emails = get_all_emails(category, sub)
    if 0 <= email_id < len(emails):
        return emails[email_id]
    return None

def delete_emails_by_ids(category: str, ids: List[int], sub: str = "general"):
    data = _load_data()
    if category not in data or sub not in data[category]:
        return

    for idx in sorted(ids, reverse=True):
        if 0 <= idx < len(data[category][sub]):
            del data[category][sub][idx]

    _save_data(data)
