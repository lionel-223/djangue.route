from typing import Type

from . import session


def add(table, keys=None, **kwargs):
    keys = keys or {}
    keys |= kwargs
    result = table(**keys)
    session.add(result)
    session.commit()
    #TODO use the logging lib
    print('Added', result, 'to db')


def get_or_create(
    table: Type,
    search_keys: dict = None,
    create_keys=None,
    include_search_in_create=True,
    **kwargs,
) -> object:
    search_keys = search_keys or {}
    search_keys |= kwargs
    result = session.query(table).filter_by(**search_keys).first()
    if not result:
        create_keys = create_keys or {}
        if include_search_in_create:
            create_keys = search_keys | create_keys
        add(table, create_keys)
    return result
