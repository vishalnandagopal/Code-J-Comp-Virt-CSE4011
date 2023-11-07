FROM python:3.12

LABEL virt-flask-app image

ADD ./requirements.txt ./requirements.txt

RUN ["pip3","install","-r","requirements.txt"]

RUN ["pip3", "install", "gunicorn"]

WORKDIR /virt-jcomp

ENV PYTHONUNBUFFERED=1

COPY . .

CMD gunicorn --bind 0.0.0.0:8000 --workers 3 wsgi:app