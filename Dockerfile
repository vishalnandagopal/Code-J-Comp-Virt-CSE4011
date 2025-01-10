FROM python:3.12-alpine AS runtime-image

LABEL virt-flask-app image

ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

RUN ["pip","install","gunicorn"]

RUN ["pip","install","--requirement","requirements.txt"]

WORKDIR /virt-jcomp

COPY . .

ENV PYTHONUNBUFFERED=1

CMD gunicorn --bind 0.0.0.0:8000 --workers 3 wsgi:app
