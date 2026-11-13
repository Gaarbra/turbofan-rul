# Learning path

| Step | What I learn | Check it worked |
| --- | --- | --- |
| 1. Load the data | What one row of engine data means | `scripts/step1_load.py` prints engine 1 |
| 2. Compute RUL | RUL = last cycle of an engine minus current cycle | `pytest` passes |
| 3. Look at sensors | Which sensors change as an engine wears out | A plot of 3 sensors for one engine |
| 4. Baseline model | Predict RUL with a simple model | An error number on held-out engines |
| 5. Store in SQLite | Query engines with SQL | One query that returns engine lifetimes |

## Where I am

Steps 1 and 2 have starter code. Steps 3 to 5 are not started.

## Questions I still have

- Why split train and test by engine and not by row?
- Why cap RUL at a maximum value in many papers?
