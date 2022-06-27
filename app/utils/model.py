import inspect
import typing

class Model:
    """
    Helper class for easily looking up data in dicts and converting them using
    a dataclass-like structure

    This is inspired by Pydantic and I will probably publish it as a standalone
    Python package on PyPI at some point, so I'm plugging my GitHub here:
        https://github.com/Tina-otoge/

    example:
    some_dict = {'id': '1982', 'postal_code': 12345}

    class AddressModel(Model):
        id = int
        zipcode = Model.getter('postal_code', type=str)

    address = AddressModel(some_dict)
    address.id == 1982
    address.zipcode == '12345'

    AddressModel.dict(some_dict) -> {'id': 1982, 'zipcode': '12345'}
    """
    __AUTO_STR__ = True
    __ERROR_ON_UNFOUND__ = False

    @classmethod
    def _get(cls, d: dict, key):
        if cls.__ERROR_ON_UNFOUND__:
            return d[key]
        return d.get(key)

    @staticmethod
    def exists(x):
        return x != None

    @staticmethod
    def true(x):
        return bool(x)

    @classmethod
    def getter(cls, key=None, type=None, cond=None, default='_none') -> typing.Callable:
        def f(d: dict, _model_key=None):
            _key = key or _model_key
            value = cls._get(d, _key)
            if type and (cond is None or cond(value)):
                value = type(value)
            elif default != '_none':
                value = default
            return value
        return f

    @staticmethod
    def const(value):
        def f(_d: dict):
            return value
        return f

    @classmethod
    def str(cls, key=None, lower=False):
        def f(x: str):
            if not x:
                return x
            x = x.strip()
            if lower:
                x = x.lower()
            return x
        return cls.getter(key=key, type=f)

    @classmethod
    def dict(cls, d: dict) -> dict:
        result = {}
        parents_keys = set()
        for parent in cls.mro()[1:-1]:
            for attr in dir(parent):
                parents_keys.add(attr)
        for key in dir(cls):
            if key in parents_keys:
                continue
            type = getattr(cls, key)
            if cls.__AUTO_STR__ and type == str:
                type = cls.str()
            if not isinstance(type, typing.Type) and callable(type):
                if '_model_key' in inspect.signature(type).parameters:
                    value = type(d, _model_key=key)
                else:
                    value = type(d)
            else:
                value = type(cls._get(d, key))
            result[key] = value
        return result

    def __init__(self, d: dict):
        self.dict = self.dict(d)
        for key, value in self.dict.items():
            setattr(self, key, value)

    def __repr__(self):
        name = self.__class__.__name__
        attrs = ', '.join([
            f'{key}={value}'
            for key, value
            in self.dict.items()
        ])
        return f'<{name} {attrs}>'
