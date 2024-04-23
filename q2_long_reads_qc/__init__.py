from ._version import get_versions

# from .fastMultiQC_stats import fastMultiQC_stats
from .nanoplot_stats import stats
from .trim_long_reads import chop

__version__ = get_versions()["version"]
del get_versions

# __all__ = ["fastMultiQC_stats", "chop", "stats"]
__all__ = ["chop", "stats"]
