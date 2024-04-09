from ._version import get_versions
from .fastMultiQC_stats import fastMultiQC_stats
from .nanoplot_stats import nanoplot_stats
from .trim_long_reads import trim_long_reads

__version__ = get_versions()["version"]
del get_versions

__all__ = ["fastMultiQC_stats", "trim_long_reads", "nanoplot_stats"]
