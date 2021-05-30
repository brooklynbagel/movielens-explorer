import os
import time

from flask import Flask, jsonify, request
from flask_cors import CORS

import click
import pymysql

import helpers
import query_prep

app = Flask(__name__)
CORS(app)


db = pymysql.connect(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    database=os.getenv("DB_NAME"),
)


MAX_RESULTS = 10


@app.route("/test")
def test():
    with db.cursor() as cur:
        cur.execute("SELECT col FROM test;")
        (result,) = cur.fetchone()
        return jsonify(dict(result=result, backend="python"))


@app.cli.command("load-movielens")
def load_movielens():
    with db.cursor() as cur:
        cur.execute("SELECT col FROM test;")
        (result,) = cur.fetchone()
        click.echo(f"result {result}")


@app.route("/echo")
def echo():
    keywords = request.args.getlist("keywords[]")
    data = dict(keywords=keywords)
    return jsonify(data)


@app.route("/query")
def query():
    with db.cursor() as cur:
        t0 = time.perf_counter()
        select = query_prep.build_select(request.args)
        query = select["query"]
        args = select["args"]
        try:
            cur.execute(query, args)
            result = cur.fetchall()
        except pymysql.Error as e:
            app.logger.error(e)
            app.logger.error(cur.mogrify(query, args))
            return jsonify({}), 500
        except pymysql.Warning as w:
            app.logger.warning(w)
            app.logger.warning(cur.mogrify(query, args))

        movies = [helpers.prepare_movie_object(row) for row in result]

        dt = time.perf_counter() - t0
        app.logger.info("query made had %s results (%0.3f secs)", len(movies), dt)
        return jsonify(movies)
