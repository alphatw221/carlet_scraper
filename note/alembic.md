alembic init migrations

alembic revision --autogenerate -m "update"
alembic upgrade head