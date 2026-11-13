# Turbofan Engine Maintenance

I am learning how to predict when a jet engine will fail, using NASA's
C-MAPSS simulated engine data. Each engine runs until it fails, and sensors
record every cycle. The goal is to predict Remaining Useful Life (RUL): how
many cycles are left.

This is a learning project. See [LEARNING.md](LEARNING.md) for the steps.

## Setup

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install pandas pytest
.venv\Scripts\python scripts/download_data.py
.venv\Scripts\python scripts/step1_load.py
.venv\Scripts\python -m pytest
```

Data source: [NASA C-MAPSS](https://data.nasa.gov/dataset/cmapss-jet-engine-simulated-data).
The data is not stored in this repo. `download_data.py` fetches it.
