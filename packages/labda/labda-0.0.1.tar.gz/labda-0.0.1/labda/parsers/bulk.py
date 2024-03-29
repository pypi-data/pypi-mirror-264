from pathlib import Path
from typing import Callable

from labda.structure import Collection

# TODO: Add bulk parsing with linkage file
# TODO: Add parallel processing of files.


def bulk_parser(folder: str | Path, parser: Callable, id: str | None = None, **kwargs):
    if isinstance(folder, str):
        folder = Path(folder)

    if not folder.is_dir():
        raise ValueError(f"'{folder}' is not a valid folder.")

    files = list(Path(folder).glob("*"))

    if id is None:
        id = folder.name

    collection = Collection(id=id)

    for file in files:
        try:
            subject = parser(file, **kwargs)
            collection.add_subject(subject)
        except Exception as e:
            print(f"Error while parsing | {file} | {e}")  # TODO: Log error

    return collection
