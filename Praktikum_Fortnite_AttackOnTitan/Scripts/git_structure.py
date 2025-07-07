import json
import os
import csv

# Load a Revision Snapshot
def load_snapshot(file_path):
    with open(file_path,'r', encoding='utf-8' ) as f:
        return json.load(f)

# compare two revisions 
def compare_revisions(claims_old, claims_new, user_old, user_new, ownership, additions, removals, modifications): 
    old_keys = set(claims_old.keys())  # set of predicates in claims 
    new_keys = set(claims_new.keys())
    # if we have multiple predicates changed , added or deleted the increse is done by the number of additions, deletions and modifications because we have to for loop
    #  Additions (predicates only in new)
    for predicate in new_keys - old_keys:  
        ownership[predicate] = user_new  # New predicate is owned by user_new
        additions[user_new] = additions.get(user_new, 0) + 1  # increase number of additions of user_new by one
    
    #  Removals (predicates only in old)
    for predicate in old_keys - new_keys:
        owner = ownership.get(predicate, user_old)
        removals[(user_new, owner)] = removals.get((user_new, owner), 0) + 1
        ownership.pop(predicate, None)
     
     #  Modifications (predicate exists in both but values differ)    
    for predicate in old_keys & new_keys:
        if claims_old[predicate] != claims_new[predicate]:
            owner = ownership.get(predicate, user_old)
            modifications[(user_new, owner)] = modifications.get((user_new, owner), 0) + 1
            ownership[predicate] = user_new  # Transfer ownership to the new user

# loop over all pairs of revisions and compare them 
def process_entity_revisions(revision_id_csv, snapshot_folder):
    ownership = {}
    additions = {}
    removals = {}
    modifications = {}

    # Read revision rows in correct chronological order from CSV
    with open(revision_id_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    for i in range(len(rows) - 1):
        rev_id_old = rows[i]["rev_id"]
        rev_id_new = rows[i + 1]["rev_id"]

        user_old = rows[i]["user"]
        user_new = rows[i + 1]["user"]

        # Build the file paths to the JSON snapshot files for each revision
        file_old = os.path.join(snapshot_folder, f"revision_{rev_id_old}.json")
        file_new = os.path.join(snapshot_folder, f"revision_{rev_id_new}.json")

        try:
            with open(file_old, "r", encoding="utf-8") as f1:
                data_old = json.load(f1)

            with open(file_new, "r", encoding="utf-8") as f2:
                data_new = json.load(f2)

            claims_old = list(data_old["entities"].values())[0].get("claims", {})
            claims_new = list(data_new["entities"].values())[0].get("claims", {})

            compare_revisions(
                claims_old, claims_new,
                user_old, user_new,
                ownership, additions, removals, modifications
            )

        except Exception as e:
            # Handle any unexpected issues (missing file, bad format, etc.)
            print(f" Skipped pair ({rev_id_old}, {rev_id_new}) due to error: {e}")  

    return additions, removals, modifications          

def save_git_dictionaries(additions, removals, modifications, filename):
    """
    Save the additions, removals, and modifications dictionaries to JSON files.
    """
    dict_output_folder = f"data/git_dictionaries/{filename}"
    os.makedirs(dict_output_folder, exist_ok=True)

    with open(os.path.join(dict_output_folder, "additions.json"), "w", encoding="utf-8") as f:
        json.dump(additions, f, indent=2)

    with open(os.path.join(dict_output_folder, "removals.json"), "w", encoding="utf-8") as f:
        json.dump({f"{k[0]}->{k[1]}": v for k, v in removals.items()}, f, indent=2)

    with open(os.path.join(dict_output_folder, "modifications.json"), "w", encoding="utf-8") as f:
        json.dump({f"{k[0]}->{k[1]}": v for k, v in modifications.items()}, f, indent=2)

    print(f"📁 Saved additions, removals, and modifications for {filename} to {dict_output_folder}")


         

      