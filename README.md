# Base Development Django Environment

This is a base development environment for a Django project that uses Docker and Postgres.

Developed from docker documents [here](https://docs.docker.com/samples/django/).

## Docker commands to build and run docker containers


Build the needed files for the Postgres database and shut back down. Will be  in `DjangoApp/data` when run. 
```
docker compose -f docker-compose.dev.yml up -d db
docker compose -f docker-compose.dev.yml down db
```

Now the database files are created can run all containers.
```
docker compose -f docker-compose.dev.yml up -d
```

### Notes
Used `docker-compose.dev.yml` and `DjangoApp/Dockerfile.dev` file naming so that it highlighted the fact that this is a development environment.