import os
import subprocess as subp
import sys
from pathlib import Path

cdir = Path(__file__).parent
sys.path.append(cdir)
os.chdir(cdir)

import generate_index  # noqa

cmd = "sphinx-build -W -a -E -b html -d _build/doctrees . _build/html"

sys.exit(subp.call(cmd.split()))
