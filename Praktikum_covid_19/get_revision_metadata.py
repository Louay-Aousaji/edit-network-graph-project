import requests
import time
import csv

ENTITY_ID = "Q81068910"  # COVID-19 pandemic
API_URL = "https://www.wikidata.org/w/api.php"

params = {
    "action": "query",
    "format": "json",
    "prop": "revisions",
    "titles": ENTITY_ID,
    "rvprop": "ids|timestamp|user|comment",
    "rvslots": "main",
    "rvlimit": "max",
    "formatversion": "2"
}

revisions = []
continue_token = None

while True:
    if continue_token:
        params["rvcontinue"] = continue_token

    response = requests.get(API_URL, params=params)
    data = response.json()

    page = data["query"]["pages"][0]
    if "revisions" in page:
        revisions.extend(page["revisions"])

    if "continue" in data:
        continue_token = data["continue"]["rvcontinue"]
        time.sleep(0.5)  # avoid overloading
    else:
        break

output_file = "covid_revisions_metadata.csv"

# Save to CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["rev_id", "timestamp", "user", "comment"])
    for rev in revisions:
        writer.writerow([
            rev.get("revid", ""),
            rev.get("timestamp", ""),
            rev.get("user", ""),
            rev.get("comment", "")
        ])

print(f"✅ Done: {len(revisions)} revisions saved to {output_file}")


