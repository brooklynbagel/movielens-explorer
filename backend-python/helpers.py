import re

def prepare_movie_object(row):
    (movie_id, title, genres, imdb_id, tmdb_id, num_ratings, avg_rating) = row
    # Capture 4 digits for year and all text prior to that
    # For example, "Toy Story (1995)" gets two capture groups:
    # - "Toy Story"
    # - "1995"
    title, year = re.match("^(.+) \(([0-9]{4})\)$", title).groups()
    year = int(year)

    # Split pipe separated genres into list
    genres = genres.split("|")

    ml_url = f"https://movielens.org/movies/{movie_id}"
    imdb_url = f"https://www.imdb.com/title/tt{imdb_id}"
    tmdb_url = f"https://www.themoviedb.org/movie/{tmdb_id}"

    return dict(
        movie_id=movie_id,
        title=title,
        year=year,
        genres=genres,
        ml_url=ml_url,
        imdb_url=imdb_url,
        tmdb_url=tmdb_url,
        num_ratings=num_ratings,
        avg_rating=avg_rating
    )
