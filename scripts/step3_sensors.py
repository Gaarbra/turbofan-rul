"""Step 3: find which sensors change as engines wear out, and plot 3 for engine 1."""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "src"))
from turbofan.rul import add_rul, load

df = add_rul(load(root / "data" / "train_FD001.txt"))
sensors = [f"s{i}" for i in range(1, 22)]

flat = [s for s in sensors if df[s].std() < 1e-3]
print("flat sensors (no information):", flat)

# Correlation with RUL across all engines: strong negative = rises as engine wears.
corr = df[[s for s in sensors if s not in flat] + ["rul"]].corr()["rul"].drop("rul")
print(corr.sort_values().round(2).to_string())

top = corr.abs().sort_values(ascending=False).index[:3].tolist()
engine = df[df.unit == 1]
fig, axes = plt.subplots(len(top), 1, figsize=(7, 6), sharex=True)
for ax, s in zip(axes, top):
    ax.plot(engine["cycle"], engine[s], color="#FF8A00")
    ax.set_ylabel(s)
axes[0].set_title("Engine 1: the 3 sensors most correlated with RUL")
axes[-1].set_xlabel("cycle (engine fails at the last cycle)")
fig.tight_layout()

out = root / "docs" / "images" / "sensors.png"
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=120)
print("saved", out)
