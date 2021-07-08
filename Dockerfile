FROM ubuntu:20.04

RUN apt-get update
RUN apt-get install --no-install-recommends -y python3 python3-dev python3-pip && \
      apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

COPY ./ /app
WORKDIR /app

EXPOSE 8000
CMD gunicorn --bind 0.0.0.0:8000 wsgi
