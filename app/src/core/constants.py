import datetime as dt
from typing import Final

MOVIES_INDEX_NAME: Final[str] = "movies"
FILM_CACHE_EXPIRES: Final[dt.timedelta] = dt.timedelta(minutes=5)
GENRE_CACHE_EXPIRES: Final[dt.timedelta] = dt.timedelta(minutes=10)
PERSON_CACHE_EXPIRES: Final[dt.timedelta] = dt.timedelta(minutes=5)
