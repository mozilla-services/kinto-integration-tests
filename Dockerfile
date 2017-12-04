FROM python:alpine
RUN apk add --update make gcc git python3-dev musl-dev libffi-dev openssl-dev py-pip
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
CMD pytest --env=$TEST_ENV config-test/
