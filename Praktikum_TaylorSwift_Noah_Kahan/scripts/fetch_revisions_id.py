# fetch revision IDs from Wikidata and saves them to a .csv file

import requests
import csv
import time


def fetch_revision_id(entity_id, output_file):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "prop": "revisions",
        "titles": entity_id,
        "rvprop": "ids|user|timestamp",
        "rvlimit": "max",
        "rvdir": "newer"
    }

    revisions = []

    while True:
        response = requests.get(url, params=params)
        data = response.json()

        page = next(iter(data["query"]["pages"].values()))

        for rev in page.get("revisions", []):
            revisions.append({
                "rev_id": rev["revid"],      # ✅ Key is 'rev_id'
                "user": rev["user"],
                "timestamp": rev["timestamp"]
            })

        print(f"Collected {len(revisions)} revisions so far for {entity_id}")

        if "continue" in data:
            params.update(data["continue"])
            time.sleep(0.5)
        else:
            break

    # ✅ Save all fields
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["rev_id", "user", "timestamp"])
        for rev in revisions:
            writer.writerow([rev["rev_id"], rev["user"], rev["timestamp"]])  # ✅ Correct key

    print(f"✅ Done! Saved {len(revisions)} revision IDs to {output_file}")
