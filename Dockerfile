FROM frolvlad/alpine-python3
RUN apk add --update make gcc git python3-dev musl-dev libffi-dev openssl-dev
COPY . /app
WORKDIR /app
RUN pip3 install -r dev-requirements.txt
RUN find . -name "*.pyc" | xargs rm -rf
RUN find . -name "__pycache__" | xargs rm -rf
CMD py.test --env=stage -v /app/config-test/
