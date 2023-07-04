from uuid import uuid4


def get_uuid() -> str:
    return uuid4().hex
