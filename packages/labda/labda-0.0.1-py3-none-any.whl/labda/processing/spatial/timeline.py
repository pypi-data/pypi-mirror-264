import pandas as pd
from shapely.geometry import LineString

from ...expanders import add_distance
from ...structure.validation.subject import Column
from ...utils import convert_to_geodataframe, get_unique_column_name


def get_information(df: pd.DataFrame, crs: str) -> pd.Series:
    df = df.copy()
    start = df.index.min()
    end = df.index.max()
    duration = end - start

    distance_col = get_unique_column_name(df)
    df = add_distance(df, crs=crs, name=distance_col)
    distance = df[distance_col].sum()

    gdf = convert_to_geodataframe(df[[Column.LATITUDE, Column.LONGITUDE]], crs=crs)
    geometry = gdf["geometry"]

    # Add status and IDs based on trip_id and location_id.
    if df[Column.TRIP_ID].notna().all():
        trip_id = df[Column.TRIP_ID].iloc[0]
        if df["stationary_id"].notna().all():
            status = "pause"
            mode = pd.NA
            location_id = df["stationary_id"].iloc[0]
        else:
            status = "transport"
            mode = df["trip_mode"].iloc[0]
            location_id = pd.NA
    else:
        status = "stationary"
        trip_id = pd.NA
        mode = pd.NA
        location_id = df["stationary_id"].iloc[0]

    if status == "transport":
        geometry = LineString(geometry.tolist())  # type: ignore

    else:
        geometry = geometry.unary_union  # type: ignore

    return pd.Series(
        {
            "trip_id": trip_id,
            "stationary_id": location_id,
            "start": start,
            "end": end,
            "duration": duration,
            "distance": distance,
            "status": status,
            "mode": mode,
            "geometry": geometry,
        }
    )


def get_transport_information(df: pd.DataFrame, crs: str):
    df = df.copy()
    helper_id_col = get_unique_column_name(df)
    df.loc[~df["trip_status"].isin(["stationary", "pause"]), helper_id_col] = (
        df["trip_status"] == "start"
    ).cumsum()

    partial_trip_summaries = (
        df.groupby(helper_id_col)
        .apply(lambda x: get_information(x, crs=crs))
        .reset_index(drop=True)
    )

    return partial_trip_summaries


def get_timeline(df: pd.DataFrame, crs: str) -> pd.DataFrame:
    # TODO: Add a check for specific trip columns.
    df = df.copy()

    trips = (
        df.groupby("trip_id")
        .apply(lambda x: get_transport_information(x, crs=crs))
        .reset_index(drop=True)
    )

    stops = df.groupby("stationary_id", as_index=False).apply(
        lambda x: get_information(x, crs=crs)
    )

    summary = pd.concat([trips, stops], ignore_index=True).sort_values(["start", "end"])

    return summary.astype(
        {
            "status": "category",
            "mode": "category",
            "trip_id": "UInt16",
            "stationary_id": "UInt16",
        }
    )
