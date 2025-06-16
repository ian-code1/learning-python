import pandas as pd
import numpy as np
from collections import Counter
from datetime import datetime

def parse_line(line):
    parts = line.strip().split(" | ")
    return {
        "timestamp": parts[0],
        "Transaction_id": parts[1].split(": ")[1],
        "member": parts[2].split(": ")[1],
        "amount": int(parts[3].split(": ")[1]),
        "status": parts[4].split(": ")[1]
    }

data_list = []

with open("transactions.txt", "r") as file:
    for line in file:
        if line.strip():
            parsed = parse_line(line)
            data_list.append(parsed)

# Convert to DataFrame
df = pd.DataFrame(data_list)

# Total transactions
print("📌 Total Transactions:", len(df))

# Total amount collected (only successful)
successful_df = df[df["status"] == "SUCCESS"]
print("💰 Total Collected:", successful_df["amount"].sum())

# Unique members
print("👥 Unique Members:", df["member"].nunique())

# Status breakdown
print("✅ Successful:", (df["status"] == "SUCCESS").sum())
print("❌ Failed:", (df["status"] == "FAILED").sum())

# Extract hour
df["hour"] = df["timestamp"].apply(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S").hour)
most_common_hour = df["hour"].mode()[0]
print(f"🕐 Peak Hour: {most_common_hour}:00 hrs")

# Optional: Top 3 biggest deposits
top3 = successful_df.sort_values(by="amount", ascending=False).head(3)
print("\n🔥 Top 3 Deposits:\n", top3[["Transaction_id", "amount", "member"]])

# Optional: Save cleaned file
df.to_csv("cleaned_transactions.csv", index=False)