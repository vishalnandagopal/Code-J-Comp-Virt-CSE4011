FROM python:3.12

LABEL virt-flask-app image

RUN ["pip3","install","poetry==1.7.0"]

WORKDIR /virt-jcomp

COPY poetry.lock pyproject.toml /virt-jcomp/

RUN ["poetry","config","virtualenvs.create","false"]

RUN ["poetry","install","--no-interaction","--no-ansi"]

COPY . .

ENV PYTHONUNBUFFERED=1

CMD gunicorn --bind 0.0.0.0:8000 --workers 3 wsgi:app