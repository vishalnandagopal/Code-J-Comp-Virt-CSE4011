FROM python:3.12-alpine AS requirements-image

ENV PYTHONUNBUFFERED=1

RUN ["pip","install","poetry>=1.7,<1.8"]

RUN ["poetry","self","add","poetry-plugin-export"]

WORKDIR /export

COPY pyproject.toml poetry.lock ./

RUN ["poetry","export","--format","requirements.txt","--output","requirements.txt"]

FROM python:3.12-alpine AS runtime-image

LABEL virt-flask-app image

ENV PYTHONUNBUFFERED=1

COPY --from=requirements-image /export/requirements.txt requirements.txt

RUN ["pip","install","gunicorn"]

# RUN ["useradd","--create-home","docker-user"]

# USER docker-user

COPY requirements.txt /

RUN ["pip","install","--requirement","requirements.txt"]

WORKDIR /virt-jcomp

COPY . .

ENV PYTHONUNBUFFERED=1

CMD gunicorn --bind 0.0.0.0:8000 --workers 3 wsgi:app