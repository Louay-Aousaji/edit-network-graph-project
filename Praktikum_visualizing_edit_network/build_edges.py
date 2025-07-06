import json
import csv

#file paths
input_json = "trump_cleaned_history.json"
output_csv = "edges.csv"

#Load cleaned predicate history
with open(input_json, encoding="utf-8") as f:
    predicate_history = json.load(f)

#Build edges
edges = []
for pred, history in predicate_history.items():
    for i in range(len(history) - 1):
        rev_id_1, user_1, _ = history[i]
        rev_id_2, user_2, action_2 = history[i + 1]

        if user_1 != user_2 and action_2 in ("edit", "delete"):
            edges.append({
                "Source": user_1,
                "Target": user_2,
                "interaction_type": action_2,
                "predicate": pred,
                "revision_id": rev_id_2
            })

#Save to edges.csv
with open(output_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Source", "Target", "interaction_type", "predicate", "revision_id"])
    writer.writeheader()
    writer.writerows(edges)

print(f"Saved {len(edges)} edges to '{output_csv}'")

