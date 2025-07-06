import pandas as pd

# === Config ===
input_file = "edges_with_start_end.csv"   # Your original file
output_file = "edges_with_date_periods.csv"  # Output file name

# === Mapping from period numbers to yyyy/MM/dd ===
period_mapping = {
    1: "2020/01/01",
    2: "2022/01/01",
    3: "2024/01/01",
    4: "2025/06/29"
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


