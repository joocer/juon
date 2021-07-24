"""
Create .serialize and .parse methods to handle json operations
"""
from typing import Any, Union
import orjson

# parse is just a synonyn for loads
parse = orjson.loads

# serialize is a little more involved
def serialize(obj: Any, indent: bool = False, as_bytes: bool = False
) -> Union[str, bytes]:

    if as_bytes:
        if indent and isinstance(obj, dict):
            return orjson.dumps(
                obj, option=orjson.OPT_INDENT_2 + orjson.OPT_SORT_KEYS
            )
        else:
            return orjson.dumps(obj, option=orjson.OPT_SORT_KEYS)

    # return a string
    if indent and isinstance(obj, dict):
        return orjson.dumps(
            obj, option=orjson.OPT_INDENT_2 + orjson.OPT_SORT_KEYS
        ).decode()
    else:
        return orjson.dumps(obj, option=orjson.OPT_SORT_KEYS).decode()

