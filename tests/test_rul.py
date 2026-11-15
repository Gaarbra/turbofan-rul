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
