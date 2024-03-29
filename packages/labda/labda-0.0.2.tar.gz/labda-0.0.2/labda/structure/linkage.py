from pathlib import Path

import pandas as pd
from shapely import wkt

from .validation.linkage import SCHEMA


def from_csv(path: str | Path) -> pd.DataFrame:
    if isinstance(path, str):
        path = Path(path)

    df = pd.read_csv(
        path,
        dtype={
            "subject_id": "string",
            "sensor_id": "string",
        },
        delimiter=";",
    )

    if "start" in df.columns:
        df["start"] = pd.to_datetime(df["start"])

    if "end" in df.columns:
        df["end"] = pd.to_datetime(df["end"])

    return SCHEMA.validate(df)
