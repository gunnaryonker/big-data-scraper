import csv

input_file = "tableB.csv"
output_file = "tableBcleaned.csv"

# Define the same schema order for the cleaned data
cleaned_columns = ["rank", "title", "rating", "show_type", "votes", "episodes"]

# Read data from the input file with specified encoding
with open(input_file, "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# Prepare cleaned data
cleaned_data = []
for row in data:
    cleaned_row = {
        "rank": row["rank_id"],
        "title": row["title"],
        "rating": row["rating"],
        "show_type": row["show_type"],
        "votes": row["votes"],
        "episodes": row["episodes"]
    }
    cleaned_data.append(cleaned_row)

# Write cleaned data to the output file in csv and save
with open(output_file, "w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=cleaned_columns)
    writer.writeheader()
    writer.writerows(cleaned_data)

# Print out completion with file name
print("Data cleaning complete. Cleaned data saved as", output_file)
