import json
import csv
from collections import defaultdict
from itertools import combinations

# === Config ===
history_file = "trump_cleaned_history.json"
edges_file = "trump_coedit_edges.csv"
nodes_file = "trump_coedit_nodes.csv"
threshold = 10  # Minimum number of shared predicates

# === Load predicate history ===
with open(history_file, encoding="utf-8") as f:
    predicate_history = json.load(f)

# === Count shared predicates per user pair ===
coedit_counts = defaultdict(int)

for history in predicate_history.values():
    users = [entry[1] for entry in history]
    unique_users = set(users)
    for user_a, user_b in combinations(sorted(unique_users), 2):
        coedit_counts[(user_a, user_b)] += 1

# === Build edge list and gather users who meet threshold ===
valid_edges = []
involved_users = set()

for (user_a, user_b), count in coedit_counts.items():
    if count >= threshold:
        valid_edges.append((user_a, user_b, count))
        involved_users.update([user_a, user_b])

# === Write edges.csv ===
with open(edges_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Source", "Target", "Weight"])
    writer.writeheader()
    for src, tgt, weight in valid_edges:
        writer.writerow({
            "Source": src,
            "Target": tgt,
            "Weight": weight
        })

# === Write nodes.csv ===
with open(nodes_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Id", "Label"])
    writer.writeheader()
    for user in sorted(involved_users):
        writer.writerow({
            "Id": user,
            "Label": user
        })

print(f"✅ Saved {len(valid_edges)} edges to '{edges_file}'")
print(f"✅ Saved {len(involved_users)} nodes to '{nodes_file}'")

