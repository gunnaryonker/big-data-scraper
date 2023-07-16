import csv

def calculate_length_stats(data_file, attribute):
    total_length = 0
    min_length = float('inf')
    max_length = 0
    min_title = ''
    max_title = ''
    num_values = 0

    with open(data_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            value = row[attribute]
            length = len(value)
            total_length += length
            if length < min_length:
                min_length = length
                min_title = value
            if length > max_length:
                max_length = length
                max_title = value
            num_values += 1

    average_length = total_length / num_values

    return average_length, min_length, min_title, max_length, max_title

# Specify the csv file to open
data_file = 'tableAcleaned.csv'

# Specify the title column to count characters
attribute = 'title'

# Calculate length statistics and get min/max titles
average_length, min_length, min_title, max_length, max_title = calculate_length_stats(data_file, attribute)

# Print the results of the average length, minimum length and title, max length and title
print(f"Average length of '{attribute}': {average_length:.2f} characters")
print(f"Minimum length of '{attribute}': {min_length} characters")
print(f"Minimum title: {min_title}")
print(f"Maximum length of '{attribute}': {max_length} characters")
print(f"Maximum title: {max_title}")
