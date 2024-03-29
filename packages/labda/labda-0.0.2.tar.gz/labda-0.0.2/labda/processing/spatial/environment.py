import pandas as pd

# TODO: Refactor...


def detect_environment(
    df: pd.DataFrame,
    algorithm: str = "palms",
    *,
    name: str = "environment",
    overwrite: bool = False,
    **kwargs,
) -> pd.DataFrame:
    if name in df.columns and not overwrite:
        raise ValueError(f"Column '{name}' already exists in dataframe")

    df = df.copy()
    algorithms = {
        "palms": palms_environment_detection,
    }

    if algorithm not in algorithms:
        raise ValueError(f"Method must be one of {list(algorithms.keys())}.")

    df = algorithms[algorithm](df, name, **kwargs)

    return df.astype({name: "category"})


def palms_environment_detection(
    df: pd.DataFrame,
    name: str,
    method: str,
    limit: int | float | None = None,
) -> pd.DataFrame:
    if not limit:
        raise ValueError("Limit must be specified.")

    methods = ["snr_total", "nsat_ratio"]
    if method not in methods:
        raise ValueError(f"Method must be one of {methods}.")

    if method not in df.columns:
        raise ValueError(f"Column '{method}' not found in DataFrame.")

    df = df[df[method].notna()]
    df[name] = "outdoor"
    df.loc[df[method] <= limit, name] = "indoor"

    return df
