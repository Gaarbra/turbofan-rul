"""Step 5: store FD001 training data in SQLite and query engine lifetimes with SQL."""
import sqlite3
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root / "src"))
from turbofan.rul import load

db = root / "data" / "turbofan.db"
with sqlite3.connect(db) as con:
    load(root / "data" / "train_FD001.txt").to_sql("cycles", con, if_exists="replace", index=False)
    rows = con.execute(
        """
        SELECT COUNT(*)            AS engines,
               MIN(lifetime)       AS shortest,
               ROUND(AVG(lifetime)) AS average,
               MAX(lifetime)       AS longest
        FROM (SELECT unit, MAX(cycle) AS lifetime FROM cycles GROUP BY unit)
        """
    ).fetchone()
print("engines, shortest, average, longest lifetime (cycles):", rows)
print("saved", db)
