from ._version import get_versions

# from .fastMultiQC_stats import fastMultiQC_stats
from .nanoplot_stats import stats
from .trim_long_reads import trim

__version__ = get_versions()["version"]
del get_versions

__all__ = ["trim", "stats"]
