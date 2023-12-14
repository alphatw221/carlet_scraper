#!/bin/bash

cd /carlet/

python3 -m pip install poetry
poetry install

poetry run uvicorn main:app --host 0.0.0.0 --port 8002