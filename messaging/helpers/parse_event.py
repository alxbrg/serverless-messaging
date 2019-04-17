import json


def parse_event(event, prop):
    data = event.get(prop) or {}

    # deserialize if needed (e.g. for the request body)
    try:
        return json.loads(data)
    except:
        return data
