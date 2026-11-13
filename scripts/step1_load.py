"""Step 1 and 2: load FD001 training data and print engine 1 with its RUL."""
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "src"))
from turbofan.rul import add_rul, load

# TODO: if this path fails, look inside data/ and fix the folder name.
df = add_rul(load(root / "data" / "train_FD001.txt"))
print(df[df.unit == 1][["unit", "cycle", "s2", "rul"]].tail())
print("engines:", df.unit.nunique(), "rows:", len(df))
