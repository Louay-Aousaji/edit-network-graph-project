# download revision snapshots for each revision id

import requests
import json
import csv
import time
import os


# fetch a full structured snapshot of a Wikidata entity at a specific revision ID
def get_revision_snapshot(entity_id, rev_id):
    url = f"https://www.wikidata.org/wiki/Special:EntityData/{entity_id}.json?revision={rev_id}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return {}


# main function to download snapshots for a list of revision IDs (batch-safe)
def download_snapshots(entity_id, rev_csv_file, output_folder):
    revisions = []

    #  Read all revision IDs from a CSV file
    with open(rev_csv_file, newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            revisions.append(row["rev_id"])

    total_revs = len(revisions)
    batch_size = 500
    print(f" Found {total_revs} revisions for entity {entity_id}")

    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Loop over all revisions in batches
    for batch_start in range(0, total_revs, batch_size):
        batch_end = min(batch_start + batch_size, total_revs)
        batch = revisions[batch_start:batch_end]

        print(f" Downloading batch {batch_start} to {batch_end}...")

        for rev_id in batch:
            filename = os.path.join(output_folder, f"revision_{rev_id}.json")

            if os.path.exists(filename):
                continue

            json_data = get_revision_snapshot(entity_id, rev_id)
            if json_data:
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump(json_data, f, indent=2)
                print(f"✅ Saved revision {rev_id}")
            else:
                print(f"❌ Failed to fetch revision {rev_id}")

            time.sleep(0.5)
