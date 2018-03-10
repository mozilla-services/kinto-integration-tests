FROM python:alpine
RUN apk add --update make gcc python3-dev musl-dev libffi-dev openssl openssl-dev
WORKDIR /app
COPY Pipfile pipenv /app/
RUN pip install -r pipenv.txt
RUN pipenv install --system --skip-lock
COPY . /app
CMD pytest --env=$TEST_ENV
