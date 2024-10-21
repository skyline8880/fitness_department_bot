FROM python:3.11

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r requirements.txt --no-cache-dir

RUN locale-gen

COPY ./ /app

CMD python3 /app/main.py