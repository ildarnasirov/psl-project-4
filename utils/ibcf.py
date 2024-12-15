import numpy as np
import pandas as pd
from utils.movies import load_movies

def fill_user(ratings = {}, length = 3706):
    result = np.full(length, np.nan)
    for key, value in ratings.items():
        result[int(key)] = value
    
    return result

def myIBCF(user_data):
    similarity_matrix = np.load('data/trimmed_similarity_matrix.npz')['trimmed_similarity_matrix']  # Load similarity matrix from step 3
    rmat_columns = pd.read_csv('data/rmat_columns.csv', header=None).squeeze().tolist()

    new_user = fill_user(user_data, similarity_matrix.shape[0])
    w = np.array(new_user).flatten()

    # Initialize an array for predictions
    predictions = np.full(w.shape, np.nan)

    for i in range(len(w)):
        if np.isnan(w[i]):  # Only predict for movies not rated by the user
            # Find indices of similar movies that are rated by the user
            S_i = ~np.isnan(similarity_matrix[i, :])
            rated_by_user = ~np.isnan(w)
            valid_indices = np.where(S_i & rated_by_user)[0]

            # Calculate numerator and denominator for the prediction formula
            numerator = np.sum(similarity_matrix[i, valid_indices] * w[valid_indices])
            denominator = np.sum(similarity_matrix[i, valid_indices])

            # Avoid division by zero
            if denominator != 0:
                predictions[i] = numerator / denominator

    # Get the column names of the rating matrix
    movie_ids = rmat_columns

    # Create a DataFrame for predictions with movie IDs
    predictions_df = pd.DataFrame({"MovieID": movie_ids, "Prediction": predictions})
    
    # Get top 10 recommended movies based on predictions
    top_predictions = predictions_df.dropna().sort_values(by="Prediction", ascending=False).head(10)

    # If fewer than 10 recommendations, fill with most popular movies
    if len(top_predictions) < 10:
        popularity_ranking = pd.read_csv("data/popular_movies.csv") # (From System I)

        # Exclude movies already rated by the user
        rated_movies = set(np.where(~np.isnan(w))[0])
        popularity_ranking = popularity_ranking[~popularity_ranking["MovieID"].isin(rated_movies)]

        # Add remaining movies to make up the top 10
        additional_movies = popularity_ranking.head(10 - len(top_predictions))
        top_predictions = pd.concat([top_predictions, additional_movies])

    return top_predictions


def parse_recomendations (recommendations):
    return [
        int(movie.replace('m', '')) if isinstance(movie, str) else movie
        for movie in recommendations[['MovieID']].to_numpy().flatten()
    ]