import pytest

from models import Person
from services import PersonService
from tests.functional.src.factories import PersonFactory

pytestmark = pytest.mark.asyncio


async def test_get_existing_person_from_elastic(es_write_data, person_service: PersonService) -> None:
    person = PersonFactory.create()
    await es_write_data([person.model_dump(mode="json")], index=person_service.elastic_index)

    result = await person_service.get_by_id(person.id)

    assert isinstance(result, Person)
    assert result == person
    person_service.redis.get.assert_called_once_with(f"person#{person.id}")
    person_service.elastic.get.assert_called_once_with(index=person_service.elastic_index, id=str(person.id))


async def test_get_existing_person_from_redis(redis_write_data, person_service: PersonService) -> None:
    person = PersonFactory.create()
    await redis_write_data(f"person#{person.id}", person.model_dump_json())

    result = await person_service.get_by_id(person.id)

    assert isinstance(result, Person)
    assert result == person
    person_service.redis.get.assert_called_once_with(f"person#{person.id}")
    person_service.elastic.get.assert_not_called()


async def test_get_non_existing_person(redis_write_data, person_service: PersonService) -> None:
    person = PersonFactory.create()

    result = await person_service.get_by_id(person.id)

    assert result is None
    person_service.redis.get.assert_called_once_with(f"person#{person.id}")
    person_service.elastic.get.assert_called_once_with(index=person_service.elastic_index, id=str(person.id))
