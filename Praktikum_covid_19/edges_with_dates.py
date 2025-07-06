import pandas as pd

# === Config ===
input_file = "edges_with_start_end.csv"   # Your original file
output_file = "edges_with_date_periods.csv"  # Output file name

# === Mapping from period numbers to date strings ===
period_mapping = {
    1: "01/01/2020",
    2: "01/01/2022",
    3: "01/01/2024",
    4: "29/06/2025"
}

def convert_periods_to_dates(input_path, output_path):
    # Read the CSV file
    df = pd.read_csv(input_path)
    
    # Apply the date mapping
    df['start'] = df['start'].map(period_mapping)
    df['end'] = df['end'].map(period_mapping)
    
    # Save to a new CSV file
    df.to_csv(output_path, index=False)
    print(f"Converted CSV saved to: {output_path}")

# Run the conversion
convert_periods_to_dates(input_file, output_file)

