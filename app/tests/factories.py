from uuid import UUID

from faker import Faker
from faker.providers import lorem, misc, person

from models import Film, Genre, NestedPerson, NestedPersonRoles, Person

fake = Faker()

fake.add_provider(lorem)
fake.add_provider(misc)
fake.add_provider(person)


class GenreFactory:
    @classmethod
    def create(cls, id: UUID | None = None) -> Genre:
        return Genre(id=id if id is not None else fake.uuid4(), name=fake.word(), description=fake.paragraph())

    @classmethod
    def create_short(cls) -> str:
        return fake.word()


class PersonFactory:
    @classmethod
    def create(cls, id: UUID | None = None) -> Person:
        return Person(
            id=id if id is not None else fake.uuid4(),
            name=fake.name(),
            films=[PersonFactory.create_person_roles() for _ in range(fake.pyint(min_value=1, max_value=4))],
        )

    @classmethod
    def create_short(cls) -> NestedPerson:
        return NestedPerson(id=fake.uuid4(), name=fake.name())

    @staticmethod
    def create_person_roles() -> NestedPersonRoles:
        return NestedPersonRoles(
            id=fake.uuid4(), roles=[fake.word() for _ in range(fake.pyint(min_value=1, max_value=3))]
        )


class FilmFactory:
    @classmethod
    def create(cls, id: UUID = None) -> Film:
        return Film(
            id=id if id is not None else fake.uuid4(),
            title=fake.sentence(nb_words=fake.pyint(min_value=2, max_value=5)),
            imdb_rating=fake.pyfloat(left_digits=1, right_digits=1, positive=True, max_value=10),
            description=fake.paragraph(nb_sentences=fake.pyint(min_value=2, max_value=5)),
            genre=[GenreFactory.create_short() for _ in range(fake.pyint(min_value=1, max_value=3))],
            actors=[PersonFactory.create_short() for _ in range(fake.pyint(min_value=1, max_value=3))],
            writers=[PersonFactory.create_short() for _ in range(fake.pyint(min_value=1, max_value=3))],
            directors=[PersonFactory.create_short() for _ in range(fake.pyint(min_value=1, max_value=3))],
        )
