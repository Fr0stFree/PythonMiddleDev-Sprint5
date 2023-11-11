FROM python:3.11

ENV PYTHONPATH=/tests:/app/src
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY tests/ /tests


COPY app/ /app

RUN pip install --upgrade pip && \
    pip install -r /tests/requirements.test.txt && \
    pip install -r /app/requirements.txt

COPY scripts/ /scripts
