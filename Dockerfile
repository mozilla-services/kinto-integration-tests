FROM ubuntu

RUN \
    apt update -y; \
    apt upgrade -y; \
    apt install -y python-pip python-virtualenv git-core build-essential make; \
    apt install -y python python-dev libssl-dev libffi-dev; \
    git clone https://github.com/mozilla-services/services-test/ /home/services-test; \
    cd /home/services-test; \
    #pip install virtualenv; \
    apt-get clean -y; \
    chmod +x /home/services-test/kinto/run;

WORKDIR /home/services-test

# run the test
CMD ./kinto/run
