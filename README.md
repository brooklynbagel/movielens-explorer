MovieLens Explorer
===

Just a simple sample app using MariaDB, Flask and React to create a simple MovieLens movie explorer. This can be built and run using `docker-compose`:

```sh
docker compose build
docker compose up -d
```

Once started, the app can be accessed at http://localhost:3000.

There is also an alternative `docker-compose.dev.yml` file which only starts up the DB. This can be used when developing Flask and React locally:

```sh
docker compose -f docker-compose.dev.yml up -d
```
