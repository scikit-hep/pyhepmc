import subprocess as subp
from pathlib import Path
import sys  # noqa
import os

cdir = Path(__file__).parent
sys.path.append(cdir)
os.chdir(cdir)

import generate_index  # noqa

cmd = "sphinx-build -W -a -E -b html -d _build/doctrees . _build/html"

sys.exit(subp.call(cmd.split()))
