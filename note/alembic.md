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

alembic -n auto_data revision --autogenerate  -m "update"
alembic -n auto_data upgrade head


alembic -n local_carlet revision --autogenerate  -m "update"
alembic -n local_carlet upgrade head


sqlacodegen_v2 mysql+pymysql://root:carletcarlet@127.0.0.1:3306/carlet --outfile=./db/local_carlet/models.py


database-0.cluster-cqvxa7jhryy9.ap-northeast-1.rds.amazonaws.com

rd1


sqlacodegen_v2 mysql+pymysql://rd1:joX?SXII!o+,:oYve{<}@~Gy#,hl@Xo#@database-0.cluster-cqvxa7jhryy9.ap-northeast-1.rds.amazonaws.com/carlet --outfile=./db/local_carlet/models.py