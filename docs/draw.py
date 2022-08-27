import sys
import pyhepmc
from pathlib import Path

infile = Path(sys.argv[1])
outfile = Path(sys.argv[2])

with pyhepmc.open(infile) as f:
    event = f.read()

svg_code = event._repr_html_()

with open(outfile, "w") as f:
    f.write(svg_code)
