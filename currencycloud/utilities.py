import re

__all__ = ['validate_uuid4']

UUID_REGEX = re.compile(
    "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    re.I)


def validate_uuid4(uuid_string):
    return UUID_REGEX.match(uuid_string)
