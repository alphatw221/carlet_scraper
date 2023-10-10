alembic init migrations

alembic revision --autogenerate -m "update"
alembic upgrade head



alembic -n tire_rack revision --autogenerate  -m "update"
alembic -n tire_rack upgrade head