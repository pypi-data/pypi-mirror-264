import importlib.metadata

from .evaluator import Evaluator

__version__ = importlib.metadata.version("testverse")

__all__ = [Evaluator]
