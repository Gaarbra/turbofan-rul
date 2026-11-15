import pandas as pd

COLUMNS = ["unit", "cycle"] + [f"setting{i}" for i in (1, 2, 3)] + [f"s{i}" for i in range(1, 22)]


def load(path):
    """Read a C-MAPSS file. It has no header and is space separated."""
    return pd.read_csv(path, sep=r"\s+", header=None, names=COLUMNS)


def add_rul(df, cap=None):
    """Add RUL: cycles left before each engine fails (last cycle minus this cycle).

    cap: if set, RUL above it is clipped to it. Early in life the sensors barely
    change, so a model can't tell 300 cycles left from 200; capping is common.
    """
    last = df.groupby("unit")["cycle"].transform("max")
    rul = last - df["cycle"]
    return df.assign(rul=rul if cap is None else rul.clip(upper=cap))
