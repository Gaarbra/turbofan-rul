"""Step 6: do rolling averages of the sensors lower the error?

Same setup as step 4 (train FD001, score each test engine's last cycle, RUL
capped at 125). The only change: add the rolling mean of each sensor over the
last few cycles as extra features. Try a few window sizes and compare.
"""
import json
import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import root_mean_squared_error

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "src"))
from turbofan.rul import add_rolling_mean, add_rul, load

CAP = 125
data = root / "data"
train = add_rul(load(data / "train_FD001.txt"), cap=CAP)
test = load(data / "test_FD001.txt")
y_test = pd.read_csv(data / "RUL_FD001.txt", header=None)[0].clip(upper=CAP).to_numpy()

# 1. same sensors as step 4 (drop the ones that never change)
sensors = [s for s in (f"s{i}" for i in range(1, 22)) if train[s].std() > 1e-3]

results = {}
for window in [None, 5, 10, 20, 30]:
    # 2. window None = no rolling features, the step 4 random forest
    if window is None:
        name, tr, te, features = "Raw sensors only (step 4)", train, test, sensors
    else:
        name = f"Raw + rolling mean, window {window}"
        tr = add_rolling_mean(train, sensors, window)
        te = add_rolling_mean(test, sensors, window)
        features = sensors + [f"{s}_mean{window}" for s in sensors]

    # 3. roll first, then keep each test engine's last cycle, so the average uses its history
    te_last = te.groupby("unit").tail(1)
    model = RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42, n_jobs=-1)
    pred = model.fit(tr[features], tr["rul"]).predict(te_last[features])
    results[name] = round(float(root_mean_squared_error(y_test, pred)), 1)
    print(f"{name:34s} RMSE {results[name]:5.1f} cycles")

out = root / "docs" / "rolling-results.json"
out.write_text(json.dumps({"cap": CAP, "model": "random forest, 100 trees", "rmse_cycles": results}, indent=2))
print("saved", out)
