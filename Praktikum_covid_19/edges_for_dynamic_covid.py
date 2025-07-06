import pandas as pd

# Load the CSV file
df = pd.read_csv("edges_for_covid.csv")

# Convert Interval from '[1,2]' or '<1.0,2.0>' to '1.0;2.0'
def convert_interval(interval_str):
    if pd.isna(interval_str):
        return ""
    cleaned = str(interval_str).strip("[]<>").replace(" ", "")
    parts = cleaned.split(',')
    if len(parts) == 2:
        return f"{parts[0]};{parts[1]}"
    return ""

# Apply to 'Interval' (capital I)
df["Interval"] = df["Interval"].apply(convert_interval)

# Save the fixed file in the same directory
df.to_csv("edges_for_gephi_dynamic.csv", index=False)


