import enum
from typing import Type

from . import session


def add(table, keys=None, commit=True, stage=True, **kwargs):
    keys = keys or {}
    keys |= kwargs
    result = table(**keys)
    if stage:
        session.add(result)
    if stage and commit:
        session.commit()
    #TODO use the logging lib
    # print('Added', result, 'to db')
    return result


class Action:
    class States(enum.Enum):
        NOTHING = enum.auto()
        CREATED = enum.auto()
        FETCHED = enum.auto()

    value = None

    @classmethod
    def reset(cls):
        cls.value = None

    @classmethod
    def create(cls):
        cls.value = cls.States.CREATED

    @classmethod
    def fetch(cls):
        cls.value = cls.States.FETCHED

    @classmethod
    def is_created(cls):
        result = cls.value == cls.States.CREATED
        cls.reset()
        return result

    @classmethod
    def is_fetched(cls):
        result = cls.value == cls.States.FETCHED
        cls.reset()
        return result


def get_or_create(
    table: Type,
    create_keys=None,
    filter_keys: list = None,
    commit=True,
    stage=True,
    action=Action,
    **kwargs,
):
    create_keys = (create_keys or {}) | kwargs
    search_keys = {}
    filter_keys = filter_keys or []
    for key in filter_keys:
        search_keys[key] = create_keys[key]
    result = session.query(table).filter_by(**search_keys).first()
    if not result:
        create_keys = create_keys or {}
        result = add(table, create_keys, commit=commit, stage=stage)
        action.create()
    else:
        action.fetch()
    return result
