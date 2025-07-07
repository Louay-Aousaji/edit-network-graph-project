import csv

def save_nodes_csv(additions, removals, modifications, output_path):
     # Step 1: Collect all unique users from all interaction types
    all_users = set(additions.keys())
    all_users.update(u for u, _ in removals.keys())
    all_users.update(u for _, u in removals.keys())
    all_users.update(u for u, _ in modifications.keys())
    all_users.update(u for _, u in modifications.keys())

    # Step 2: Write CSV header and rows
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Id", "added_words", "WordCount", "Lat", "Long"])

        for user in all_users:
            added_count = additions.get(user, 0)  # Default to 0 if user didn't add anything
            writer.writerow([user, added_count, 0, 0, 0])
    


def save_edges_csv(additions, removals, modifications, output_path):
    
    # Save an edges CSV file showing user interactions.
   # 'ADDED' is self-loop, 'DELETED' and 'MODIFIED' are directed interactions.
 
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Source", "Target", "interaction_type", "value"])

        # Additions: self-loops
        for user, count in additions.items():
            writer.writerow([user, user, "ADDED", count])

        # Removals: directed edges with negative value
        for (user_new, user_old), count in removals.items():
            writer.writerow([user_new, user_old, "DELETED", -count])

        # Modifications: directed edges
        for (user_new, user_old), count in modifications.items():
            writer.writerow([user_new, user_old, "MODIFIED", count])
            
def expand_edges(input_path, output_path):


    with open(input_path, newline="", encoding="utf-8") as infile, \
         open(output_path, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        writer = csv.writer(outfile)

        writer.writerow(["Source", "Target", "interaction_type"])  # no "value" here, it's expanded

        for row in reader:
            source = row["Source"]
            target = row["Target"]
            interaction = row["interaction_type"]
            count = int(row["value"])

            # Repeat the row abs(count) times, handling negative values for deletions
            for _ in range(abs(count)):
                writer.writerow([source, target, interaction])

def merge_csv_with_group(file1_path, group1_name, file2_path, group2_name, output_path):
    """
    Merges node or edge CSVs, assigns groups, and filters self-loops for edges.
    """

    with open(file1_path, newline='', encoding='utf-8') as f1, \
         open(file2_path, newline='', encoding='utf-8') as f2:

        reader1 = list(csv.DictReader(f1))
        reader2 = list(csv.DictReader(f2))

        headers = reader1[0].keys()
        is_node_file = 'Id' in headers  # Heuristic: if it has 'Id', it's a nodes file

        # Add 'group' column to each row
        for row in reader1:
            row['group'] = group1_name
        for row in reader2:
            row['group'] = group2_name

        if is_node_file:
            # Merge nodes by 'Id'
            merged_nodes = {}

            for row in reader1 + reader2:
                uid = row['Id']

                if uid not in merged_nodes:
                    merged_nodes[uid] = row
                else:
                    # If user appears in both files, set group to 'both'
                    merged_nodes[uid]['group'] = 'both'

                    if 'added_words' in row:
                        merged_nodes[uid]['added_words'] = str(
                            int(merged_nodes[uid]['added_words']) + int(row['added_words'])
                        )

            fieldnames = list(merged_nodes[next(iter(merged_nodes))].keys())

            with open(output_path, 'w', newline='', encoding='utf-8') as out:
                writer = csv.DictWriter(out, fieldnames=fieldnames)
                writer.writeheader()
                for row in merged_nodes.values():
                    writer.writerow(row)

        else:
            # Edge file: Merge and filter self-loops here
            fieldnames = list(reader1[0].keys())
            with open(output_path, 'w', newline='', encoding='utf-8') as out:
                writer = csv.DictWriter(out, fieldnames=fieldnames)
                writer.writeheader()

                for row in reader1 + reader2:
                    source = row['Source']
                    target = row['Target']
                    interaction = row['interaction_type']

                    if source != target:
                        writer.writerow(row)
                    elif source == target and interaction == 'ADDED':
                        writer.writerow(row)
                    # Else: don't write the row (self-loop that is not ADDED)