import os
from .evaluator import Evaluator

print(os.getcwd())

def extract_version_from_pyproject():
    try:
        with open("../pyproject.toml", "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("version"):
                    # Assuming version is defined as: version = "x.x.x"
                    version = line.split("=")[1].strip().strip('"')
                    return version
    except:
        return None


__version__ = extract_version_from_pyproject()

__all__ = [Evaluator]
