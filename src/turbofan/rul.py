import pandas as pd

COLUMNS = ["unit", "cycle"] + [f"setting{i}" for i in (1, 2, 3)] + [f"s{i}" for i in range(1, 22)]


def load(path):
    """Read a C-MAPSS file. It has no header and is space separated."""
    return pd.read_csv(path, sep=r"\s+", header=None, names=COLUMNS)


def add_rul(df):
    """Add RUL: cycles left before each engine fails (last cycle minus this cycle)."""
    last = df.groupby("unit")["cycle"].transform("max")
    return df.assign(rul=last - df["cycle"])
