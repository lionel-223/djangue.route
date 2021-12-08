import enum


class EnumStr(enum.Enum):
    """An enum in which value and name is the same"""

    def _generate_next_value_(name, start, count, last_values):
        return name

    @classmethod
    def values(cls):
        return [x.value for x in cls]
