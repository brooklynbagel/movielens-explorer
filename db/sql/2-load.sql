USE challenge;

-- `links` table
DROP TABLE IF EXISTS links;
CREATE TABLE links(movieId INT UNSIGNED, imdbId VARCHAR(20), tmdbId VARCHAR(20), PRIMARY KEY(movieId));
LOAD DATA INFILE '/mnt/ml-latest-small/links.csv'
INTO TABLE links
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

-- `movies` table
DROP TABLE IF EXISTS movies;
CREATE TABLE movies(movieId INT UNSIGNED, title VARCHAR(300),FULLTEXT(title), genres VARCHAR(300),FULLTEXT(genres), PRIMARY KEY(movieId));
LOAD DATA INFILE '/mnt/ml-latest-small/movies.csv'
INTO TABLE movies
FIELDS TERMINATED BY ','
ENCLOSED BY '\"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

-- `ratings` table
DROP TABLE IF EXISTS ratings;
CREATE TABLE ratings(userId INT UNSIGNED, movieId VARCHAR(20), rating FLOAT UNSIGNED, timestamp BIGINT UNSIGNED, INDEX(movieId));
LOAD DATA INFILE '/mnt/ml-latest-small/ratings.csv'
INTO TABLE ratings
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

-- `tags` table
DROP TABLE IF EXISTS tags;
CREATE TABLE tags(userId INT UNSIGNED, movieId VARCHAR(20), tag VARCHAR(300),FULLTEXT(tag), timestamp BIGINT UNSIGNED, INDEX(movieId));
LOAD DATA INFILE '/mnt/ml-latest-small/tags.csv'
INTO TABLE tags
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

-- Create derived `ratings_stats` table
DROP TABLE IF EXISTS ratings_stats;
CREATE TABLE ratings_stats(movieId INT UNSIGNED, num_ratings INTEGER, avg_rating FLOAT UNSIGNED, PRIMARY KEY(movieId));
INSERT INTO ratings_stats(movieId, num_ratings, avg_rating)
SELECT movieId, COUNT(rating) AS num_ratings, AVG(rating) AS avg_rating
FROM ratings
GROUP BY movieId;

-- Create `keywords` table for search
DROP TABLE IF EXISTS keywords;
CREATE TABLE keywords(movieId INT UNSIGNED, keywords VARCHAR(300),FULLTEXT(keywords), INDEX(movieId));
-- Insert from `movies` and `tags`
INSERT INTO keywords(movieId, keywords)
(SELECT movieId, title AS keywords FROM movies)
UNION DISTINCT
(SELECT movieId, tag AS keywords FROM tags);

-- Create `users` table to match `userId`s to `movieId`s
DROP TABLE IF EXISTS users;
CREATE TABLE users(movieId INT UNSIGNED, userId VARCHAR(20), INDEX(movieId, userId));
-- Insert from `ratings` and `tags`
INSERT INTO users(movieId, userId)
(SELECT movieId, userId FROM ratings)
UNION DISTINCT
(SELECT movieId, userId FROM tags);
