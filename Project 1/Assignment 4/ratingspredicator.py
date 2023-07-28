import numpy as np
import pandas as pd
from scipy.spatial.distance import cosine

# Load the ratings_small_test.csv datasets using pandas
training_data = pd.read_csv('ratings_small_training.csv')
test_data = pd.read_csv('ratings_small_test.csv')

# Create a user-item matrix where rows represent users, columns represent movies, and cells contain the ratings
user_item_matrix = training_data.pivot(index='userId', columns='movieId', values='rating')

# Calculate the similarity between users based on the user-item matrix
user_similarity = 1 - np.array([cosine(user_item_matrix.loc[user1], user_item_matrix.loc[user2])
                                for user1 in user_item_matrix.index for user2 in user_item_matrix.index]
                               ).reshape(user_item_matrix.shape[0], user_item_matrix.shape[0])

# Create a function to predict
def predict_rating(user_id, movie_id):
    user_ratings = user_item_matrix.loc[user_id]
    similar_users = user_similarity[user_id - 1]  # Index starts from 0

    # Filter out users who have not rated the target movie
    similar_users_ratings = user_item_matrix.iloc[np.where(~np.isnan(user_item_matrix[movie_id]))]

    if len(similar_users_ratings) == 0:
        return np.nan

    # Calculate weighted average of the ratings of similar users for the target movie
    weighted_sum = np.sum(similar_users_ratings[movie_id].values * similar_users[similar_users_ratings.index - 1])
    total_weight = np.sum(np.abs(similar_users[similar_users_ratings.index - 1]))

    if total_weight == 0:
        return np.nan
    else:
        predicted_rating = weighted_sum / total_weight
        return round(predicted_rating, 1)  # Round the rating to 1 decimal place to match the other rating formats

# Add the predicted ratings to the ratings_small_test.csv with a new rating column
test_data['rating'] = test_data.apply(lambda row: predict_rating(row['userid'], row['movieid']), axis=1)

# Save the ratings into the csv as a new column
test_data.to_csv('ratings_small_test.csv', index=False)
