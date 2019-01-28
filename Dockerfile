FROM python:alpine
RUN apk add --update make gcc python3-dev musl-dev libffi-dev openssl openssl-dev
WORKDIR /app
COPY Pipfile pipenv.txt /app/
RUN pip install -r pipenv.txt
RUN pipenv install --system --skip-lock
COPY . /app
CMD pytest -m $TEST_TYPE --env=$TEST_ENV
