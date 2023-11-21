FROM --platform=linux/x86-64 python:3.11.3-slim

COPY . /carlet
WORKDIR /carlet

RUN chmod +x ./bash/entrypoint.sh
CMD ["./bash/entrypoint.sh"]




# docker build -t yihsuehlin/carlet_api:latest -f Dockerfile .