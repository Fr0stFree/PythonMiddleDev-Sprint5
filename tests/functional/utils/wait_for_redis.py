import time
from redis import Redis

from settings import Settings

if __name__ == '__main__':
    settings = Settings()
    redis_client = Redis(host=f'{settings.redis_host}')
    while True:
        if redis_client.ping():
            print('Success connect Redis')
            break
        time.sleep(1)
