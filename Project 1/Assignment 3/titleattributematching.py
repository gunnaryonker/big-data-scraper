import pandas as pd

def create_table_c(table_a_filename, table_b_filename, output_filename):
    # Read the data from table A and table B
    table_a = pd.read_csv(table_a_filename)
    table_b = pd.read_csv(table_b_filename)

    # Perform the matching based on the data in the "title" column
    matched_pairs = pd.merge(table_a, table_b, on='title')

    # Add an ID column for each matching piece of data starting at 0
    matched_pairs['ID'] = range(len(matched_pairs))

    # Rename the columns to align with the header for table C
    matched_pairs.rename(columns={'rank_x': 'atable_rank',
                                  'rank_y': 'btable_rank',
                                  'rating_x': 'atable_rating',
                                  'rating_y': 'btable_rating',
                                  'show_type_x': 'atable_show_type',
                                  'show_type_y': 'btable_show_type',
                                  'votes_x': 'atable_votes',
                                  'votes_y': 'btable_votes',
                                  'episodes_x': 'atable_episodes',
                                  'episodes_y': 'btable_episodes'}, inplace=True)

    # Setup the columns that will be in table C
    table_c = matched_pairs[['ID', 'atable_rank', 'btable_rank', 'title', 'atable_rating', 'atable_show_type', 'atable_votes', 'btable_rating', 'atable_episodes', 
                            'btable_show_type', 'atable_votes', 'btable_episodes']]

    # Save the new table to the csv file
    table_c.to_csv(output_filename, index=False)

    # Print the total number of matches
    print("Total number of matches:", len(matched_pairs))

# csv file names, output to tableC.csv of the matching data
table_a_filename = 'tableAcleaned.csv'
table_b_filename = 'tableBcleaned.csv'
output_filename = 'tableC.csv'

# Create the table
create_table_c(table_a_filename, table_b_filename, output_filename)
