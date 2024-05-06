from ._version import get_versions

# from .fastMultiQC_stats import fastMultiQC_stats
from .nanoplot_stats import stats_paired, stats_single
from .trim_long_reads import trim_paired, trim_single

__version__ = get_versions()["version"]
del get_versions

__all__ = ["trim_single", "trim_paired", "stats_single", "stats_paired"]
