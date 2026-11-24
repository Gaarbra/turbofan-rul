# Learning path

| Step | What I learn | Check it worked |
| --- | --- | --- |
| 1. Load the data | What one row of engine data means | `scripts/step1_load.py` prints engine 1 |
| 2. Compute RUL | RUL = last cycle of an engine minus current cycle | `pytest` passes |
| 3. Look at sensors | Which sensors change as an engine wears out | A plot of 3 sensors for one engine |
| 4. Baseline model | Predict RUL with a simple model | An error number on held-out engines |
| 5. Store in SQLite | Query engines with SQL | One query that returns engine lifetimes |
| 6. Rolling averages | Smoothing noisy sensors per engine | `scripts/step6_rolling.py` prints RMSE per window |

## Where I am

All 6 steps run. Random forest RMSE is 17.3 cycles on held-out engines.
Adding rolling averages made it worse (18.1 to 21.6, see README).

## Answers so far

- Split by engine, not by row: rows from the same engine are near copies of
  each other. Splitting by row lets the model see the test engine in training,
  so the error looks better than it really is.
- Cap RUL: early in life the sensors are flat, so 300 and 200 cycles left look
  the same. Capping at 125 stops the model from being punished for that.

- Rolling averages did not help here. Every window tried (5 to 30 cycles)
  raised the error, and the result held across 5 random seeds, so it is not
  luck. I don't know why yet. The error went up for engines near failure and
  far from it, so it is not only the average lagging behind the latest wear.

## Next questions

- Why do rolling averages hurt a random forest here? Would they help linear regression?
- How does the model do on FD002 to FD004 (more operating conditions)?
