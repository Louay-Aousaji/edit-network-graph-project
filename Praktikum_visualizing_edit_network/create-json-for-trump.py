import requests
import time
import json
import csv

ENTITY_ID = "Q22686"
BATCH_START = 0 
BATCH_SIZE = 500   

# Load revision IDs from Step 1
revisions = []
with open("donald_trump_revisions.csv", newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        revisions.append(row["rev_id"])

# Function to fetch structured content
def get_revision_json(revid):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{ENTITY_ID}.json?revision={revid}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# Save content to file
batch = revisions[BATCH_START:BATCH_START + BATCH_SIZE]
for rev_id in batch:
    json_data = get_revision_json(rev_id)
    with open(f"revisions/revision_{rev_id}.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    print(f"Saved revision {rev_id}")
    time.sleep(0.5)  


