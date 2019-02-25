import json
import uuid


def flat_uuid():
    """create a flat uuid

    :return: uuid with '-' removed

    """
    return str(uuid.uuid4()).replace('-', '')


def compact_json_dict(data):
    """convert dict to compact json

    :return: str

    """
    return json.dumps(data, separators=(',', ':'), ensure_ascii=False)
