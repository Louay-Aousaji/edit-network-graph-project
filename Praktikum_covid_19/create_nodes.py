import json
import csv
from collections import defaultdict

# === File paths ===
input_json = "covid_predicate_history_cleaned.json"
output_csv = "nodes.csv"

# === Track all users and all predicate creations ===
all_users = set()
user_creation_count = defaultdict(int)

with open(input_json, encoding="utf-8") as f:
    predicate_history = json.load(f)

for predicate, history in predicate_history.items():
    for rev_id, user, action in history:
        all_users.add(user)
        if action == "create":
            user_creation_count[user] += 1

# === Write all users to CSV ===
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Id", "label", "created_predicates"])
    writer.writeheader()
    for user in sorted(all_users):
        writer.writerow({
            "Id": user,
            "label": user,
            "created_predicates": user_creation_count.get(user, 0)
        })

print(f"✅ Saved {len(all_users)} nodes to '{output_csv}'")


