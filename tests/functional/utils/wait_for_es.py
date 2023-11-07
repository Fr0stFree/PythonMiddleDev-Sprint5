import time
from elasticsearch import Elasticsearch

from settings import Settings

if __name__ == '__main__':
    settings = Settings()
    es_client = Elasticsearch(hosts=f'http://{settings.elastic_host}:{settings.elastic_port}')
    while True:
        if es_client.ping():
            print('Success connect Elasticsearch')
            break
        time.sleep(1)