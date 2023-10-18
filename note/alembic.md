alembic init migrations

alembic revision --autogenerate -m "update"
alembic upgrade head



alembic -n tire_rack revision --autogenerate  -m "update"
alembic -n tire_rack upgrade head


alembic -n autofiles revision --autogenerate  -m "update"
alembic -n autofiles upgrade head

alembic -n paintscratch revision --autogenerate  -m "update"
alembic -n paintscratch upgrade head

alembic -n automobiledimension revision --autogenerate  -m "update"
alembic -n automobiledimension upgrade head


