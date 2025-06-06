# twX
alembic revision --autogenerate -m "create tables"

docker exec -i twx-db-1 psql -U user -d twX -c 'SELECT * FROM "tokens";'

`docker exec -i twx-db-1 psql -U user -d twX -c 'TRUNCATE TABLE "alembic_version", "users", "tokens" RESTART IDENTITY CASCADE;'
`