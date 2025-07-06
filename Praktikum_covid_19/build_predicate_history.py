import os
import json
from collections import defaultdict

# === Configuration ===
ENTITY_ID = "Q81068910"  # COVID-19 pandemic
JSON_FOLDER = "covid_jsons"  # Folder with all JSON revision files
OUTPUT_FILE = "covid_predicate_history.json"

# === Helper to extract predicates from a JSON revision ===
def extract_predicates(json_data):
    try:
        claims = json_data["entities"][ENTITY_ID]["claims"]
        return {pred: json.dumps(values, sort_keys=True) for pred, values in claims.items()}
    except KeyError:
        return {}

# === Step 1: Load and sort all revision files ===
revision_files = sorted(os.listdir(JSON_FOLDER), key=lambda f: int(f.split("_")[1].split(".")[0]))

predicate_histories = defaultdict(list)
prev_predicate_state = {}

# === Step 2: Compare revisions and build predicate history ===
for filename in revision_files:
    path = os.path.join(JSON_FOLDER, filename)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    rev_id = filename.split("_")[1].split(".")[0]
    user = data["entities"][ENTITY_ID].get("lastrevid_user", "unknown")

    current_predicate_state = extract_predicates(data)
    all_preds = set(prev_predicate_state) | set(current_predicate_state)

    for pred in all_preds:
        prev_val = prev_predicate_state.get(pred)
        curr_val = current_predicate_state.get(pred)

        if prev_val is None and curr_val is not None:
            predicate_histories[pred].append((rev_id, user, "create"))
        elif prev_val is not None and curr_val is None:
            predicate_histories[pred].append((rev_id, user, "delete"))
        elif prev_val != curr_val:
            predicate_histories[pred].append((rev_id, user, "edit"))

    prev_predicate_state = current_predicate_state

# === Step 3: Save to JSON ===
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(predicate_histories, f, indent=2)

print(f"✅ Done. Saved predicate history to '{OUTPUT_FILE}'")


