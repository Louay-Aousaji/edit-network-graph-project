import os
import json
from collections import defaultdict

ENTITY_ID = "Q4152"  # or Q37200
JSON_FOLDER = "castle_jsons"  # or pyramid_jsons

# Output: {predicate: [(rev_id, user, action_type)]}
predicate_histories = defaultdict(list)

# Helper to extract predicates from a JSON revision
def extract_predicates(json_data):
    try:
        claims = json_data["entities"][ENTITY_ID]["claims"]
        return {pred: json.dumps(values, sort_keys=True) for pred, values in claims.items()}
    except KeyError:
        return {}

# Load and sort all revision files
revision_files = sorted(os.listdir(JSON_FOLDER), key=lambda f: int(f.split("_")[1].split(".")[0]))

prev_predicate_state = {}

for filename in revision_files:
    path = os.path.join(JSON_FOLDER, filename)
    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    rev_id = filename.split("_")[1].split(".")[0]
    try:
        user = list(data["entities"][ENTITY_ID]["lastrevid_user"].values())[0]  # fallback if 'user' not in top-level
    except:
        user = data["entities"][ENTITY_ID].get("lastrevid_user", "unknown")

    current_predicate_state = extract_predicates(data)

    # Set of all predicates in either state
    all_preds = set(prev_predicate_state) | set(current_predicate_state)

    for pred in all_preds:
        prev_val = prev_predicate_state.get(pred)
        curr_val = current_predicate_state.get(pred)

        if prev_val is None and curr_val is not None:
            # Predicate was added
            predicate_histories[pred].append((rev_id, user, "create"))
        elif prev_val is not None and curr_val is None:
            # Predicate was deleted
            predicate_histories[pred].append((rev_id, user, "delete"))
        elif prev_val != curr_val:
            # Predicate was modified
            predicate_histories[pred].append((rev_id, user, "edit"))
        # else: unchanged, skip

    prev_predicate_state = current_predicate_state

# Save or return predicate_histories for next steps
print(f"✅ Done. Parsed {len(revision_files)} revisions and found {len(predicate_histories)} predicates.")

import json
with open("castle_predicate_history.json", "w", encoding="utf-8") as f:
    json.dump(predicate_histories, f)



