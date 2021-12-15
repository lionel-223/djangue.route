from typing import Type
from sqlalchemy import orm

from app.utils import str_format


class Base:
    @orm.declared_attr
    def __tablename__(cls: Type):
        """
        Generate table names from class names converted from CamelCase to lower
        snake_case, with an added "s" or "ies" if it end with "y"

        Examples:
        - User -> users
        - UserSetting -> user_settings
        - Country -> countries
        """
        name = str_format.camel_to_snake(cls.__name__)
        if name.endswith('y'):
            return name[:-1] + 'ies'
        return name + 's'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
