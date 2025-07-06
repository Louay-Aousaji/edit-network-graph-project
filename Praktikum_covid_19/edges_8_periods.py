import json
import csv
from datetime import datetime, timedelta

# === File paths ===
history_file = "covid_predicate_history_cleaned.json"
metadata_file = "covid_revisions_metadata.csv"
output_file = "edges_8_periods.csv"

# === Load revision metadata ===
rev_id_to_time = {}
with open(metadata_file, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        rev_id = row["rev_id"]
        ts_str = row["timestamp"]
        try:
            ts = datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ")
            rev_id_to_time[rev_id] = ts
        except:
            continue

# === Compute 8 time periods ===
sorted_times = sorted(rev_id_to_time.values())
start_time = sorted_times[0]
end_time = sorted_times[-1]
total_days = (end_time - start_time).days
step = total_days // 8

period_bounds = []
for i in range(9):  # 9 boundaries = 8 periods
    period_bounds.append(start_time + timedelta(days=i * step))

# === Helper to get period bounds ===
def get_period_bounds(ts):
    for i in range(8):
        if period_bounds[i] <= ts < period_bounds[i + 1]:
            start = period_bounds[i].strftime("%Y/%m/%d")
            end = period_bounds[i + 1].strftime("%Y/%m/%d")
            return start, end
    return None, None  # timestamp after last period

# === Load predicate history ===
with open(history_file, encoding="utf-8") as f:
    predicate_history = json.load(f)

# === Create edges ===
edges = []
for predicate, history in predicate_history.items():
    if len(history) < 2:
        continue

    for i in range(1, len(history)):
        rev_id_prev, user_a, action_a = history[i - 1]
        rev_id_curr, user_b, action_b = history[i]

        if user_a == user_b:
            continue

        timestamp = rev_id_to_time.get(rev_id_curr)
        if timestamp is None:
            continue

        start, end = get_period_bounds(timestamp)
        if start is None:
            continue

        edges.append({
            "Source": user_a,
            "Target": user_b,
            "Type": "Directed",
            "Label": "edit_flow",
            "Predicate": predicate,
            "start": start,
            "end": end
        })

# === Save to CSV ===
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Source", "Target", "Type", "Label", "Predicate", "start", "end"])
    writer.writeheader()
    writer.writerows(edges)

print(f"✅ Saved {len(edges)} edges to '{output_file}'")
