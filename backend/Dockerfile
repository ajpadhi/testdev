FROM dockerhub.cisco.com/docker.io/python:3.11-slim-bookworm as requirements-stage

RUN pip install poetry
COPY ./pyproject.toml ./poetry.lock /
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --without=dev --with=prod

FROM dockerhub.cisco.com/docker.io/python:3.11-slim-bookworm

COPY --from=requirements-stage /requirements.txt /requirements.txt
COPY ./pyproject.toml ./gunicorn_conf.py /
COPY ./app /app

RUN python3 -m pip install --no-cache-dir --upgrade -r requirements.txt

ENV PORT 8000
EXPOSE 8000

RUN mkdir -p /tmp/shm
RUN mkdir /.local
RUN chown -R 1001:0 /.local /app /tmp/shm
RUN chmod -R 777 /tmp /app

USER 1001

ENTRYPOINT ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-c", "gunicorn_conf.py", "app.main:app"]
