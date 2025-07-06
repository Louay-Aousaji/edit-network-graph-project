import pandas as pd
import json
from collections import defaultdict
from pathlib import Path

# === Load files ===
pyramid_history = json.load(open("pyramid_predicate_history.json", encoding="utf-8"))
castle_history = json.load(open("castle_predicate_history.json", encoding="utf-8"))

pyramid_meta = pd.read_csv("pyramid_revisions_metadata.csv")
castle_meta = pd.read_csv("castle_revisions_metadata.csv")

# === Build rev_id → user mapping ===
pyramid_rev_user = dict(zip(pyramid_meta["rev_id"].astype(str), pyramid_meta["user"]))
castle_rev_user = dict(zip(castle_meta["rev_id"].astype(str), castle_meta["user"]))

# === Replace "unknown" with actual usernames ===
def clean_history(history, rev_user_map):
    cleaned = {}
    for pred, entries in history.items():
        cleaned[pred] = []
        for rev_id, _, action in entries:
            user = rev_user_map.get(rev_id, "unknown")
            cleaned[pred].append((rev_id, user, action))
    return cleaned

pyramid_clean = clean_history(pyramid_history, pyramid_rev_user)
castle_clean = clean_history(castle_history, castle_rev_user)

# === Process histories to build nodes and edges ===
user_info = defaultdict(lambda: {"created": set(), "entities": set()})
edges = []

def process_history(history, entity_id):
    for pred, changes in history.items():
        for i, (rev_id, user, action) in enumerate(changes):
            user_info[user]["entities"].add(entity_id)
            if action == "create":
                user_info[user]["created"].add(pred)
                edges.append((user, user, "create", pred, entity_id, rev_id))
            elif i > 0:
                prev_user = changes[i - 1][1]
                if user != prev_user:
                    edges.append((prev_user, user, action, pred, entity_id, rev_id))

process_history(pyramid_clean, "Q37200")
process_history(castle_clean, "Q4152")

# === Build nodes.csv ===
nodes = []
for user, info in user_info.items():
    if info["entities"] == {"Q37200"}:
        color = "blue"
    elif info["entities"] == {"Q4152"}:
        color = "red"
    else:
        color = "green"
    nodes.append({
        "Id": user,
        "Label": user,
        "added_predicates": len(info["created"]),
        "entity_color": color
    })

# === Build DataFrames ===
nodes_df = pd.DataFrame(nodes)
edges_df = pd.DataFrame(edges, columns=["Source", "Target", "interaction_type", "predicate", "entity", "revision_id"])

# === Export ===
output_dir = Path("gephi_output")
output_dir.mkdir(exist_ok=True)

nodes_df.to_csv(output_dir / "nodes.csv", index=False)
edges_df.to_csv(output_dir / "edges.csv", index=False)

print("✅ Exported nodes.csv and edges.csv to: gephi_output/")

