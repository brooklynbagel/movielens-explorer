from copy import deepcopy

from query_prep import keywords_filter, pagination_filter, genres_filter, user_id_filter, movie_name_filter

SQL = dict(
    query=["movies.movieId IN (SELECT movieId FROM keywords WHERE MATCH(keywords) AGAINST(%s))"],
    args=["funny animation"]
)


class TestKeywordsFilter:
    sql = dict(query=[], args=[])
    expected = SQL


    def test_filter_does_not_mutate_inputs(self):
        self.sql_copy = deepcopy(self.sql)
        keywords_filter(self.sql, ["funny", "animation"])
        assert self.sql_copy == self.sql


    def test_filter_is_idempotent(self):
        res1 = keywords_filter(self.sql, ["funny", "animation"])
        res2 = keywords_filter(self.sql, ["funny", "animation"])
        assert res1 == res2


    def test_keywords_filter_works(self):
        assert keywords_filter(self.sql, ["funny", "animation"]) == self.expected


    def test_filter_keeps_query_and_args_length_same(self):
        res = keywords_filter(self.sql, ["funny", "animation"])
        assert len(res["query"]) == len(res["args"])


class TestPaginationFilter:
    sql = SQL
    expected = dict(
        query=[
            "movies.movieId IN (SELECT movieId FROM keywords WHERE MATCH(keywords) AGAINST(%s))",
            "movies.movieId > %s"
        ],
        args=[
            "funny animation",
            "5678"
        ]
    )


    def test_filter_does_not_mutate_inputs(self):
        self.sql_copy = deepcopy(self.sql)
        pagination_filter(self.sql, 5678)
        assert self.sql_copy == self.sql


    def test_filter_is_idempotent(self):
        res1 = pagination_filter(self.sql, 5678)
        res2 = pagination_filter(self.sql, 5678)
        assert res1 == res2


    def test_pagination_filter_works(self):
        assert pagination_filter(self.sql, 5678) == self.expected


    def test_filter_keeps_query_and_args_length_same(self):
        res = pagination_filter(self.sql, 5678)
        assert len(res["query"]) == len(res["args"])


class TestGenresFilter:
    sql = SQL

    expected1 = dict(
        query=[
            "movies.movieId IN (SELECT movieId FROM keywords WHERE MATCH(keywords) AGAINST(%s))",
            "movies.genres LIKE %s"
        ],
        args=[
            "funny animation",
            "%Action%"
        ]
    )

    expected2 = dict(
        query=[
            "movies.movieId IN (SELECT movieId FROM keywords WHERE MATCH(keywords) AGAINST(%s))",
            "movies.genres LIKE %s",
            "movies.genres LIKE %s"
        ],
        args=[
            "funny animation",
            "%Action%",
            "%Comedy%"
        ]
    )


    def test_filter_does_not_mutate_inputs(self):
        self.sql_copy = deepcopy(self.sql)
        genres_filter(self.sql, ["Action", "Comedy"])
        assert self.sql_copy == self.sql


    def test_filter_is_idempotent(self):
        res1 = genres_filter(self.sql, ["Action", "Comedy"])
        res2 = genres_filter(self.sql, ["Action", "Comedy"])
        assert res1 == res2


    def test_genres_filter_works(self):
        assert genres_filter(self.sql, []) == self.sql
        assert genres_filter(self.sql, ["Action"]) == self.expected1
        assert genres_filter(self.sql, ["Action", "Comedy"]) == self.expected2


    def test_genres_filter_keeps_query_and_args_lengths_same(self):
        res = genres_filter(self.sql, [])
        assert len(res["query"]) == len(res["args"])

        res = genres_filter(self.sql, ["Action"])
        assert len(res["query"]) == len(res["args"])

        res = genres_filter(self.sql, ["Action", "Comedy"])
        assert len(res["query"]) == len(res["args"])


class TestUserIdFilter:
    sql = SQL

    expected = dict(
        query=[
            "movies.movieId IN (SELECT movieId FROM keywords WHERE MATCH(keywords) AGAINST(%s))",
            "movies.movieId IN (SELECT movieId FROM users WHERE userId = %s)"
        ],
        args=[
            "funny animation",
            "1234"
        ]
    )


    def test_filter_does_not_mutate_inputs(self):
        self.sql_copy = deepcopy(self.sql)
        user_id_filter(self.sql, "1234")
        assert self.sql_copy == self.sql


    def test_filter_is_idempotent(self):
        res1 = user_id_filter(self.sql, "1234")
        res2 = user_id_filter(self.sql, "1234")
        assert res1 == res2


    def test_user_id_filter_works(self):
        assert user_id_filter(self.sql, None) == self.sql
        assert user_id_filter(self.sql, "1234") == self.expected


    def test_filter_keeps_query_and_args_length_same(self):
        res = user_id_filter(self.sql, None)
        assert len(res["query"]) == len(res["args"])

        res = user_id_filter(self.sql, "1234")
        assert len(res["query"]) == len(res["args"])


class TestMovieNameFilter:
    sql = SQL

    expected = dict(
        query=[
            "movies.movieId IN (SELECT movieId FROM keywords WHERE MATCH(keywords) AGAINST(%s))",
            "movies.title LIKE %s"
        ],
        args=[
            "funny animation",
            "%Toy Story%"
        ]
    )


    def test_filter_does_not_mutate_inputs(self):
        self.sql_copy = deepcopy(self.sql)
        movie_name_filter(self.sql, "Toy Story")
        assert self.sql_copy == self.sql


    def test_filter_is_idempotent(self):
        res1 = movie_name_filter(self.sql, "Toy Story")
        res2 = movie_name_filter(self.sql, "Toy Story")
        assert res1 == res2


    def test_movie_name_filter_works(self):
        assert movie_name_filter(self.sql, None) == self.sql
        assert movie_name_filter(self.sql, "Toy Story") == self.expected


    def test_filter_keeps_query_and_args_length_same(self):
        res = movie_name_filter(self.sql, None)
        assert len(res["query"]) == len(res["args"])

        res = movie_name_filter(self.sql, "Toy Story")
        assert len(res["query"]) == len(res["args"])
