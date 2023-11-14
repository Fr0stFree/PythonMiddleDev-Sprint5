import asyncio
from functools import wraps
import logging

logger = logging.getLogger(__name__)


def backoff(exceptions=None, start_sleep_time=3, factor=2, border_sleep_time=10, retry_count=10):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка. Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param exceptions: список ошибок при которых стоит делать повторные попытки
    :param retry_count: максимальное кол-во попыток
    :return: результат выполнения функции
    """
    def func_wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            sleep_time = start_sleep_time
            tries = 0
            while True:
                try:
                    tries += 1
                    return await func(*args, **kwargs)
                except Exception as e:
                    if tries >= retry_count:
                        raise e
                    if exceptions and type(e) not in exceptions:
                        raise e
                    logger.info(f'Connection error {e}.Retrying...')
                    await asyncio.sleep(sleep_time)
                    sleep_time *= factor
                    sleep_time = min(sleep_time, border_sleep_time)

        return inner
    return func_wrapper
