from ._version import get_versions
from .quality_control import aggregate_results

__version__ = get_versions()["version"]
del get_versions

__all__ = ["aggregate_results"]
