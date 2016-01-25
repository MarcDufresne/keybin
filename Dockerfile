FROM ubuntu
MAINTAINER MarcDufresne

EXPOSE 5000

RUN apt-get -y update && apt-get -y install build-essential python2.7-dev python-pip libffi-dev
RUN mkdir /app

WORKDIR /app

ADD store_api /app/store_api
COPY setup.py /app/setup.py

RUN python setup.py install
RUN pip install uwsgi

COPY store.cfg /app/store.cfg

CMD ["uwsgi", "-s", "0.0.0.0:5000", "--protocol=http", "-w", "store_api.main:app", "-p", "10", "--pythonpath", "/app"]
