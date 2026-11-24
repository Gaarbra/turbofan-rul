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


def add_rolling_mean(df, columns, window):
    """Add a rolling mean of each column, computed inside each engine.

    Sensors are noisy from cycle to cycle. Averaging the last `window` cycles
    smooths the noise so the wear trend is easier to see. groupby("unit") keeps
    one engine's cycles from mixing into the next engine's average.
    min_periods=1: the first cycles average over however many exist so far.
    """
    rolled = df.groupby("unit")[columns].transform(lambda c: c.rolling(window, min_periods=1).mean())
    return df.join(rolled.add_suffix(f"_mean{window}"))
