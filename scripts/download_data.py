"""Download and unzip the NASA C-MAPSS data into data/."""
import io
import urllib.request
import zipfile
from pathlib import Path

URL = "https://phm-datasets.s3.amazonaws.com/NASA/6.+Turbofan+Engine+Degradation+Simulation+Data+Set.zip"
out = Path(__file__).resolve().parent.parent / "data"
out.mkdir(exist_ok=True)
with urllib.request.urlopen(URL) as r:
    outer = zipfile.ZipFile(io.BytesIO(r.read()))
# The NASA zip holds a second zip (CMAPSSData.zip). Open that one.
inner = next(n for n in outer.namelist() if n.endswith("CMAPSSData.zip"))
zipfile.ZipFile(io.BytesIO(outer.read(inner))).extractall(out)
print("saved to", out)
