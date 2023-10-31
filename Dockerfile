FROM python:3.12

LABEL virt image

WORKDIR /virt

COPY . .

RUN ["pip3","install","-r","requirements.txt"]

CMD python3 app.py