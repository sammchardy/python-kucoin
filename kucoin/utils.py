import json
import uuid
import asyncio

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


def get_loop():
    """check if there is an event loop in the current thread, if not create one
    inspired by https://stackoverflow.com/questions/46727787/runtimeerror-there-is-no-current-event-loop-in-thread-in-async-apscheduler
    """
    try:
        loop = asyncio.get_event_loop()
        return loop
    except RuntimeError as e:
        if str(e).startswith("There is no current event loop in thread"):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop
        else:
            raise
