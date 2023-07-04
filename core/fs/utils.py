import filetype


def get_file_extension(image_stream: bytes) -> str | None:

    kind = filetype.guess(image_stream)
    if kind:
        return kind.extension

    return None


def get_file_mime(image_stream: bytes) -> str | None:

    kind = filetype.guess(image_stream)
    if kind:
        return kind.mime

    return None
