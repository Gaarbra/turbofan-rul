"""Step 4: predict RUL on held-out engines and report the error.

Train on train_FD001. Score on test_FD001: those engines are cut off before
failure, and RUL_FD001 holds the true RUL at each engine's last recorded cycle.
Train and test are different engines, so the model never sees a test engine.
"""
import json
import sys
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "src"))
from turbofan.rul import add_rul, load

CAP = 125
data = root / "data"
train = add_rul(load(data / "train_FD001.txt"), cap=CAP)
test_last = load(data / "test_FD001.txt").groupby("unit").tail(1)
y_test = pd.read_csv(data / "RUL_FD001.txt", header=None)[0].clip(upper=CAP).to_numpy()

sensors = [f"s{i}" for i in range(1, 22)]
features = [s for s in sensors if train[s].std() > 1e-3]

models = {
    "Mean of training RUL": None,
    "Linear regression": LinearRegression(),
    "Random forest (100 trees)": RandomForestRegressor(n_estimators=100, min_samples_leaf=5, random_state=42, n_jobs=-1),
}
results = {}
for name, model in models.items():
    if model is None:
        pred = [train["rul"].mean()] * len(y_test)
    else:
        pred = model.fit(train[features], train["rul"]).predict(test_last[features])
    results[name] = round(float(root_mean_squared_error(y_test, pred)), 1)
    print(f"{name:28s} RMSE {results[name]:5.1f} cycles")

print(f"\n{len(train.unit.unique())} train engines, {len(y_test)} test engines, RUL capped at {CAP}")
out = root / "docs" / "baseline-results.json"
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps({"cap": CAP, "features": features, "rmse_cycles": results}, indent=2))
print("saved", out)
