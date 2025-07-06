import requests
import time
import json
import os
import csv

ENTITY_ID = "Q81068910"
CSV_FILE = "covid_revisions_metadata.csv"
OUTPUT_FOLDER = "covid_jsons"
BATCH_START = 3500       # change this to resume if interrupted
BATCH_SIZE = 176       # number of revisions to download

# Ensure output folder exists
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
# Load revision IDs
revisions = []
with open(CSV_FILE, newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        revisions.append(row["rev_id"])

# Function to fetch one revision's JSON
def get_revision_json(revid):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{ENTITY_ID}.json?revision={revid}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return {}

# Download in batches
batch = revisions[BATCH_START:BATCH_START + BATCH_SIZE]
for rev_id in batch:
    json_data = get_revision_json(rev_id)
    with open(f"{OUTPUT_FOLDER}/revision_{rev_id}.json", "w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)
    print(f"✅ Saved revision {rev_id}")
    time.sleep(0.5)


