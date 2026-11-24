import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from turbofan.rul import add_rul


def test_rul_counts_down_to_zero_per_engine():
    df = pd.DataFrame({"unit": [1, 1, 1, 2, 2], "cycle": [1, 2, 3, 1, 2]})
    assert add_rul(df)["rul"].tolist() == [2, 1, 0, 1, 0]


def test_rul_cap_clips_only_high_values():
    df = pd.DataFrame({"unit": [1, 1, 1, 1], "cycle": [1, 2, 3, 4]})
    assert add_rul(df, cap=2)["rul"].tolist() == [2, 2, 1, 0]


def test_rolling_mean_stays_inside_each_engine():
    from turbofan.rul import add_rolling_mean

    df = pd.DataFrame({"unit": [1, 1, 1, 2, 2], "s1": [2.0, 4.0, 6.0, 10.0, 20.0]})
    out = add_rolling_mean(df, ["s1"], window=2)
    # engine 2 starts fresh at 10, it does not average with engine 1's last value
    assert out["s1_mean2"].tolist() == [2.0, 3.0, 5.0, 10.0, 15.0]
