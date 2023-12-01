FROM python:3.12-slim

LABEL virt-flask-app image

COPY requirements.txt /

RUN ["pip","install","-r","requirements.txt"]

WORKDIR /virt-jcomp

COPY . .

ENV PYTHONUNBUFFERED=1

CMD gunicorn --bind 0.0.0.0:8000 --workers 3 wsgi:app