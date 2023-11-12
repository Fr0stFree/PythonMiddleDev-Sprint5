from core.config import Settings


class TestSettings(Settings):
    app_persons_endpoint: str = "persons"
    app_genres_endpoint: str = "genres"
    app_films_endpoint: str = "films"
