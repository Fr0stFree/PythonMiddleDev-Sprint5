import datetime as dt
from typing import Final

MOVIES_INDEX_NAME: Final[str] = "movies"
FILM_CACHE_EXPIRE: Final[dt.timedelta] = dt.timedelta(minutes=5)
