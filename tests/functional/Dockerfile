FROM python:3.11

ENV PYTHONPATH=./
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./ /tests/functional/


RUN pip install -r /tests/functional/requirements.txt
