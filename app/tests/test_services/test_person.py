from unittest.mock import Mock
from uuid import UUID

from elastic_transport import ApiResponseMeta
from elasticsearch import NotFoundError
from faker import Faker

from models import Person
from services import PersonService

from ..factories import PersonFactory

fake = Faker()


async def test_get_existing_person_from_elastic(person_service: PersonService) -> None:
    looking_person_id = UUID(fake.uuid4())
    person_service.redis.get.return_value = None
    person_service.elastic.get.return_value = {"_source": PersonFactory.create(id=looking_person_id).model_dump()}

    person = await person_service.get_by_id(looking_person_id)

    assert isinstance(person, Person)
    assert person.id == looking_person_id
    person_service.redis.get.assert_awaited_once_with(f"person#{person.id}")
    person_service.elastic.get.assert_awaited_once_with(index=PersonService.elastic_index, id=str(looking_person_id))


async def test_get_existing_person_from_redis(person_service: PersonService) -> None:
    looking_film_id = UUID(fake.uuid4())
    person_service.redis.get.return_value = PersonFactory.create(id=looking_film_id).model_dump_json()

    person = await person_service.get_by_id(looking_film_id)

    assert isinstance(person, Person)
    assert person.id == looking_film_id
    person_service.redis.get.assert_awaited_once_with(f"person#{person.id}")
    person_service.elastic.get.assert_not_awaited()


async def test_get_non_existing_person(person_service: PersonService) -> None:
    looking_film_id = UUID(fake.uuid4())
    person_service.redis.get.return_value = None
    person_service.elastic.get.side_effect = NotFoundError(message="", meta=Mock(spec_set=ApiResponseMeta), body={})

    person = await person_service.get_by_id(looking_film_id)

    assert person is None
    person_service.redis.get.assert_awaited_once_with(f"person#{looking_film_id}")
    person_service.elastic.get.assert_awaited_once_with(index=PersonService.elastic_index, id=str(looking_film_id))


async def test_get_many_persons_from_elastic(person_service: PersonService) -> None:
    person_service.redis.exists.return_value = False
    person_service.elastic.search.return_value = {
        "hits": {
            "hits": [
                {"_source": PersonFactory.create().model_dump()},
                {"_source": PersonFactory.create().model_dump()},
            ]
        }
    }

    persons = await person_service.get_many(query={}, params={})

    assert len(persons) == 2
    assert all(isinstance(person, Person) for person in persons)
    person_service.redis.exists.assert_awaited_once()
    person_service.redis.lrange.assert_not_awaited()
    person_service.elastic.search.assert_awaited_once_with(index=PersonService.elastic_index, query={}, params={})


async def get_many_persons_from_redis(person_service: PersonService) -> None:
    person_service.redis.exists.return_value = True
    person_service.redis.lrange.return_value = [
        PersonFactory.create().model_dump_json(),
        PersonFactory.create().model_dump_json(),
    ]

    persons = await person_service.get_many(query={}, params={})

    assert len(persons) == 2
    assert all(isinstance(person, Person) for person in persons)
    person_service.redis.exists.assert_awaited_once()
    person_service.redis.lrange.assert_awaited_once()
    person_service.elastic.search.assert_not_awaited()


async def get_non_existing_persons(person_service: PersonService) -> None:
    person_service.redis.exists.return_value = False
    person_service.elastic.search.return_value = {"hits": {"hits": []}}

    persons = await person_service.get_many(query={}, params={})

    assert persons == []
    person_service.redis.exists.assert_awaited_once()
    person_service.redis.lrange.assert_not_awaited()
    person_service.elastic.search.assert_awaited_once_with(index=PersonService.elastic_index, query={}, params={})
