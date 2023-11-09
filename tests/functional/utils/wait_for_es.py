import time
from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

if __name__ == '__main__':
    es_client = Elasticsearch(hosts=f'http://{os.getenv("ELASTIC_HOST")}:{os.getenv("ELASTIC_PORT")}')
    while True:
        if es_client.ping():
            print('Success connect Elasticsearch')
            break
        time.sleep(1)
