import pandas as pd

# Load your existing edges file
df = pd.read_csv("edges_for_covid.csv")

# Extract start and end from '[1,2]' or '<1.0,2.0>'
def extract_start_end(interval_str):
    if pd.isna(interval_str):
        return None, None
    cleaned = str(interval_str).strip("[]<>").replace(" ", "")
    parts = cleaned.split(',')
    if len(parts) == 2:
        return float(parts[0]), float(parts[1])
    return None, None

# Apply extraction
df[['start', 'end']] = df['Interval'].apply(lambda x: pd.Series(extract_start_end(x)))

# Optional: drop old Interval column
df.drop(columns=['Interval'], inplace=True)

# Save new version
df.to_csv("edges_with_start_end.csv", index=False)

