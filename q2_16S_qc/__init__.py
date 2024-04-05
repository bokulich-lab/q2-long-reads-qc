from ._version import get_versions
from .aggregate_results import aggregate_results
from .trim import trim

__version__ = get_versions()["version"]
del get_versions

__all__ = ["aggregate_results", "trim"]
