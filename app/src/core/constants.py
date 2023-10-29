import datetime as dt
from typing import Final

MOVIES_INDEX_NAME: Final[str] = "movies"
PERSONS_INDEX_NAME: Final[str] = "persons"
GENRES_INDEX_NAME: Final[str] = "genres"
FILM_CACHE_EXPIRE: Final[dt.timedelta] = dt.timedelta(minutes=5)
