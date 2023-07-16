import csv

input_file = "tableAcleaned.csv"

# Read data from the input file
with open(input_file, "r") as file:
    reader = csv.DictReader(file)
    data = [row for row in reader]

# Count blank values in each column to check for missing data
blank_counts = {}
for row in data:
    for column, value in row.items():
        if value == "":
            if column in blank_counts:
                blank_counts[column] += 1
            else:
                blank_counts[column] = 1

# Print the blank value counts, blank if none
print("Blank Value Counts:")
for column, count in blank_counts.items():
    print(f"{column}: {count}")
