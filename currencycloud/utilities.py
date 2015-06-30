import re
import uuid

__all__ = ['validate_uuid4']

UUID_REGEX = re.compile(
    "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
    re.I)


def old_validate_uuid4(uuid_string):
    return UUID_REGEX.match(uuid_string)

def validate_uuid4(uuid_string):
    try:
        val = uuid.UUID(uuid_string, version=4)
    except ValueError:
        return False
    return str(val) == uuid_string
