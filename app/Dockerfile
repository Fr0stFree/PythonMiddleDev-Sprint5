FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY ./src .


EXPOSE 8000

CMD ["gunicorn", "--workers=4", "--bind=127.0.0.1:8000", "main:app"]
