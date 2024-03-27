from .evaluator import Evaluator
import importlib.metadata

__version__ = importlib.metadata.version("testverse")

__all__ = [Evaluator]
