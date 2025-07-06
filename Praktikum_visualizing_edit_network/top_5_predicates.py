import json
import requests
import csv
from collections import defaultdict, Counter

# === Load predicate history ===
with open("trump_cleaned_history.json", encoding="utf-8") as f:
    history = json.load(f)

# === Count actions per predicate and per user ===
predicate_action_count = {}
predicate_user_counts = {}

for predicate, actions in history.items():
    total = 0
    user_counter = Counter()
    for rev_id, user, action in actions:
        total += 1
        user_counter[user] += 1
    predicate_action_count[predicate] = total
    predicate_user_counts[predicate] = user_counter

# === Get top 5 most edited predicates ===
top_predicates = sorted(predicate_action_count.items(), key=lambda x: x[1], reverse=True)[:5]

# === Get labels (real names) using Wikidata API ===
def get_label(pid):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{pid}.json"
    try:
        r = requests.get(url).json()
        return r["entities"][pid]["labels"]["en"]["value"]
    except:
        return "Unknown"

# === Prepare CSV ===
with open("top_5_controversial_predicates.csv", "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Predicate", "Label", "Total Actions", "Top Contributor 1", "Count 1", "Top Contributor 2", "Count 2", "Top Contributor 3", "Count 3"])

    for predicate, total in top_predicates:
        label = get_label(predicate)
        top_users = predicate_user_counts[predicate].most_common(3)
        row = [predicate, label, total]
        for user, count in top_users:
            row.extend([user, count])
        # Fill if less than 3 users
        while len(row) < 9:
            row.extend(["", ""])
        writer.writerow(row)

print("✅ Saved top_5_controversial_predicates.csv")

