FROM python:alpine
RUN apk add --update make gcc python3-dev musl-dev libffi-dev openssl openssl-dev
WORKDIR /app
RUN pip install pipenv
COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --system
COPY . /app
CMD pytest --env=$TEST_ENV
