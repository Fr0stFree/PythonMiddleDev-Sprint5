FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt requirements.txt

RUN  pip install --upgrade pip \
     && pip install --no-cache-dir -r requirements.txt

COPY ./src .

EXPOSE 8080

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]