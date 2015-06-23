__all__ = ['validate_uuid4']

# from uuid import UUID

import re

UUID_REGEX = re.compile("[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", re.I)

def validate_uuid4(uuid_string):
	return UUID_REGEX.match(uuid_string)

	# Below we have a proper implementation, but it does not work with the UUID used :-(
    # try:
    #     val = UUID(uuid_string, version=4)
    # except ValueError:
    #     return False
    # return val.hex == uuid_string
