import json
import csv

# === Input paths ===
predicate_file = "covid_predicate_history.json"
metadata_file = "covid_revisions_metadata.csv"
output_file = "covid_predicate_history_cleaned.json"

# === Load revision metadata ===
rev_id_to_user = {}
with open(metadata_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rev_id = row["rev_id"]
        user = row["user"]
        rev_id_to_user[rev_id] = user

# === Load predicate history ===
with open(predicate_file, encoding="utf-8") as f:
    predicate_history = json.load(f)

# === Replace unknowns ===
replaced_count = 0
for predicate, history in predicate_history.items():
    for entry in history:
        rev_id, user, action = entry
        if user == "unknown":
            corrected_user = rev_id_to_user.get(rev_id, "unknown")
            if corrected_user != "unknown":
                entry[1] = corrected_user
                replaced_count += 1

# === Save the updated file ===
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(predicate_history, f, indent=2)

print(f"✅ Done. Replaced {replaced_count} unknown users.")
print(f"📁 Cleaned file saved as: {output_file}")

