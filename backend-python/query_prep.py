from copy import deepcopy
from typing import Optional

MAX_ROWS = 10

def keywords_filter(sql: dict[str, list[str]],
                    keywords: list[str],
                    ) -> dict[str, list[str]]:
    if keywords:
        sql = deepcopy(sql)
        sql["query"].append("movies.movieId IN (SELECT movieId FROM keywords WHERE MATCH(keywords) AGAINST(%s))")
        sql["args"].append(" ".join(keywords))
    return sql


def pagination_filter(sql: dict[str, list[str]],
                      max_id: int
                      ) -> dict[str, list[str]]:
    if max_id > 0:
        sql = deepcopy(sql)
        sql["query"].append("movies.movieId > %s")
        sql["args"].append(str(max_id))
    return sql


def genres_filter(sql: dict[str, list[str]],
                  genres: list[str]
                  ) -> dict[str, list[str]]:
    if genres:
        sql = deepcopy(sql)
        sql["query"].extend("movies.genres LIKE %s" for genre in genres)
        sql["args"].extend(f"%{genre}%" for genre in genres)
    return sql


def user_id_filter(sql: dict[str, list[str]],
                   user_id: Optional[str]
                   ) -> dict[str, list[str]]:
    if user_id:
        sql = deepcopy(sql)
        sql["query"].append("movies.movieId IN (SELECT movieId FROM users WHERE userId = %s)")
        sql["args"].append(user_id)
    return sql


def movie_name_filter(sql: dict[str, list[str]],
                      movie_name: Optional[str]
                      ) -> dict[str, list[str]]:
    if movie_name:
        sql = deepcopy(sql)
        sql["query"].append("movies.title LIKE %s")
        sql["args"].append(f"%{movie_name}%")
    return sql


def build_where_clause(request_args):
    where_clause = dict(query=list(), args=list())

    # required keywords search
    keywords: list[str] = request_args.getlist("keywords[]")
    where_clause = keywords_filter(where_clause, keywords)

    # required pagination filter
    max_id: int = request_args.get("max_id", 0, type=int)
    where_clause = pagination_filter(where_clause, max_id)

    # optional filters

    # genres filter
    genres: list[str] = request_args.getlist("genres[]")
    where_clause = genres_filter(where_clause, genres)

    # user_id filter
    user_id: Optional[str] = request_args.get("userId")
    where_clause = user_id_filter(where_clause, user_id)

    # movie_name filter
    movie_name: Optional[str] = request_args.get("movieName")
    where_clause = movie_name_filter(where_clause, movie_name)

    where_clause["query"] = " AND ".join(where_clause["query"])
    where_clause["query"] = f"WHERE {where_clause['query']}"
    return where_clause


def build_select(request_args):
    where_clause = build_where_clause(request_args)
    query = f"""SELECT
movies.movieId, movies.title, movies.genres,
links.imdbId, links.tmdbId,
ratings_stats.num_ratings, ratings_stats.avg_rating
FROM movies
LEFT JOIN links ON movies.movieId = links.movieId
LEFT JOIN ratings_stats ON movies.movieId = ratings_stats.movieId
{where_clause["query"]}
ORDER BY movies.movieId
LIMIT {MAX_ROWS};"""
    return dict(query=query, args=where_clause["args"])
