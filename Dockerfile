FROM frolvlad/alpine-python3
RUN apk add --update make gcc git python3-dev musl-dev libffi-dev openssl-dev
COPY . /app
WORKDIR /app
CMD tox
