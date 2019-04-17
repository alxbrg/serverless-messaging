import json


def parse_event(event, prop):
    return event.get(prop) or {}
