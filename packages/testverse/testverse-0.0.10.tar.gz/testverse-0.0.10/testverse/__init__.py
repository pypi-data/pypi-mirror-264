from .evaluator import Evaluator


def extract_version_from_pyproject():
    with open("pyproject.toml", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("version"):
                # Assuming version is defined as: version = "x.x.x"
                version = line.split("=")[1].strip().strip('"')
                return version
    return None


__version__ = extract_version_from_pyproject()

__all__ = [Evaluator]
