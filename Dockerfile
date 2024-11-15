# Dockerfile
FROM python:3.12-rc-slim-buster

WORKDIR /app

COPY app/ .

RUN pip install --upgrade pip

RUN pip install setuptools

RUN pip install flask
 
CMD ["python", "app.py"]