from scripts.fetch_revisions_id import fetch_revision_id
from scripts.download_revision import download_snapshots
from scripts.git_structure import process_entity_revisions, save_git_dictionaries
from scripts.generate_graph_csv import save_edges_csv
from scripts.generate_graph_csv import save_nodes_csv, expand_edges, merge_csv_with_group
import os

def run_entity(name, qid):
    print(f"fetching revisions id for : {name} ({qid})")
    filename = name.lower().replace(" ", "_")
    output_path = f"data/revisions_id/{filename}.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fetch_revision_id(qid, output_path)

    snapshot_dir = f"data/revisions/{name}"
    os.makedirs(snapshot_dir, exist_ok=True)

    # download_snapshots(qid, output_path, snapshot_dir)

    json_files = [
        f for f in os.listdir(snapshot_dir)
        if f.endswith(".json") and f.startswith("revision_")
    ]
    print(f" Total snapshots saved for {name}: {len(json_files)}") 

    #  Process Git-like structure (additions, removals, modifications)
    print(f" Comparing revisions for: {name}")
    additions, removals, modifications = process_entity_revisions(output_path, snapshot_dir)
    save_git_dictionaries(additions, removals, modifications, filename)

    # Generate CSV files for nodes and edges
    edges_output_path = f"data/graph_edges/{filename}_edges.csv"
    nodes_output_path = f"data/graph_nodes/{filename}_nodes.csv"
    os.makedirs(os.path.dirname(edges_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(nodes_output_path), exist_ok=True)

    save_edges_csv(additions, removals, modifications, edges_output_path)
    save_nodes_csv(additions, removals, modifications, nodes_output_path)
    print(f" Saved graph CSV files for {name}")
     
    # Expand edges
    expanded_edges_file = f"data/graph_edges/{filename}_edges_expanded.csv"
    expand_edges(edges_output_path, expanded_edges_file)
    print(f" Expanded edges saved for {name} at {expanded_edges_file}")

def main():
    # Set your two specific entities here
    entities = {
        "Fortnite": "Q349375",
    "Attack_on_Titan": "Q586025"
    }

    for name, qid in entities.items():
        run_entity(name, qid)

   
    e1, e2 = "Taylor_Swift", "Noah_Kahan"
    f1, f2 = e1.lower().replace(" ", "_"), e2.lower().replace(" ", "_")

    nodes1 = f"data/graph_nodes/{f1}_nodes.csv"
    nodes2 = f"data/graph_nodes/{f2}_nodes.csv"
    edges1 = f"data/graph_edges/{f1}_edges_expanded.csv"
    edges2 = f"data/graph_edges/{f2}_edges_expanded.csv"

    merged_nodes_path = f"data/graph_nodes/{f1}_{f2}_merged_nodes.csv"
    merged_edges_path = f"data/graph_edges/{f1}_{f2}_merged_edges.csv"

    merge_csv_with_group(nodes1, f1, nodes2, f2, merged_nodes_path)
    merge_csv_with_group(edges1, f1, edges2, f2, merged_edges_path)

    print(f"\n🔗 Merged NODES file saved at:     {merged_nodes_path}")
    print(f"🔗 Merged EDGES file saved at:     {merged_edges_path}")
    print("✅ Merge complete — you can now import both into Gephi.")

if __name__ == "__main__":
    main()
