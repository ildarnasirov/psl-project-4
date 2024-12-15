import pandas as pd
import requests
from utils.constants import FULL_STAR, EMPTY_STAR

def load_movies ():
    movie_lines = requests \
        .get('https://liangfgithub.github.io/MovieData/movies.dat?raw=true').text \
        .split('\n')

    movie_data = []
    for i in range (len(movie_lines)):
        if not movie_lines[i]:
            continue

        line_data = movie_lines[i].split('::')
        movie_data.append(
            line_data + [f'https://liangfgithub.github.io/MovieImages/{line_data[0]}.jpg']
        )

    # Create a DataFrame from the movie data
    movies = pd.DataFrame(movie_data, columns=['movie_id', 'title', 'genres', 'url'])
    movies['movie_id'] = movies['movie_id'].astype(int)
    return movies

def count_stars (value):
    return value.count(FULL_STAR)

def generate_stars (value, max_rating = 5):
    return f"{(FULL_STAR * min(value, max_rating))}{EMPTY_STAR * max(max_rating - value, 0)}"
