
import os, sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if path not in sys.path:
    sys.path.append(path)
    os.chdir(path)

