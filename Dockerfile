FROM python:alpine
RUN apk add --update make gcc g++ python3-dev musl-dev libffi-dev openssl openssl-dev
WORKDIR /app
RUN pip install --progress-bar=off -U pip && \
    pip install poetry
COPY pyproject.toml poetry.lock /app/
RUN poetry install --no-dev --no-interaction --verbose
COPY . /app
CMD poetry run pytest -m $TEST_TYPE --env=$TEST_ENV
