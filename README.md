# twX

## Get started

1. `docker compose up --build`
2. `alembic revision --autogenerate -m "create tables"`







## useful commands

### Print this before the first migration:
alembic revision --autogenerate -m "create tables"

### Chek table values
`docker exec -i twx-db-1 psql -U user -d twX -c 'SELECT * FROM "tokens";'`

### Clear tables values
`docker exec -i twx-db-1 psql -U user -d twX -c 'TRUNCATE TABLE "alembic_version", "users", "tokens" RESTART IDENTITY CASCADE;'`