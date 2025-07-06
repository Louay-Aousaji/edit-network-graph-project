import csv
import json

# File paths
csv_path = "donald_trump_revisions.csv"
input_json = "trump_predicate_history.json"
output_json = "trump_cleaned_history.json"

#Step 1: Build rev_id → user dictionary from CSV
rev_id_to_user = {}
with open(csv_path, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        rev_id_to_user[row["rev_id"]] = row["user"]

#Step 2: Load predicate history
with open(input_json, encoding="utf-8") as f:
    predicate_history = json.load(f)

# Step 3: Replace "unknown" users
for pred, history in predicate_history.items():
    for i, (rev_id, user, action) in enumerate(history):
        if user == "unknown":
            corrected_user = rev_id_to_user.get(rev_id, "unknown")
            history[i] = [rev_id, corrected_user, action]

#Step 4: Save cleaned predicate history
with open(output_json, "w", encoding="utf-8") as f:
    json.dump(predicate_history, f, indent=2)

print(f"✅ Saved cleaned predicate history to '{output_json}'")

