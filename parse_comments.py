import pandas as pd
import json
import os
import glob
# 1. Load the JSON file (Make sure the filename matches exactly what Google gave you)
# Usually it's 'my-comments.json'
# file_path = 'my-comments.json'
# Since i received a folder of CSVs, lets combine these multiple csvs first
csv_files = glob.glob("comments*.csv")

def merge_my_comments(files):
    all_dfs = []
    
    for file in files:
        print(f"Reading {file}...")
        # 2. Read the CSV (Google uses UTF-8 encoding for comments)
        temp_df = pd.read_csv(file, encoding='utf-8')
        all_dfs.append(temp_df)
    
    # 3. Stack all the dataframes on top of each other
    master_df = pd.concat(all_dfs, ignore_index=True)

    # 4. Clean up: Rename columns for easier use if needed
    # Google usually provides: 'Content', 'PublishedAt', 'VideoUrl'
    return master_df

if __name__ == "__main__":
    if not csv_files:
        print("No CSV files found! Make sure they are in this folder.")
    else:
        master_data = merge_my_comments(csv_files)
        
        # 5. Save the combined version
        master_data.to_csv('my_full_history.csv', index=False)
        
        print(f"\nSuccess! Merged {len(csv_files)} files.")
        print(f"Total comments found: {len(master_data)}")
        print("\n--- Preview ---")
        print(master_data.head())