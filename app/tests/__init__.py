import sys
import pathlib

# add project root
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))