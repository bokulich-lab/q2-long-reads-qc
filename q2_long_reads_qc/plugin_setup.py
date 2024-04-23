# ----------------------------------------------------------------------------
# Copyright (c) 2024, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from q2_types.per_sample_sequences import (
    PairedEndSequencesWithQuality,
    SequencesWithQuality,
)
from q2_types.sample_data import SampleData
from qiime2.plugin import Citations, Int, Plugin, Range

import q2_long_reads_qc
from q2_long_reads_qc import __version__
from q2_long_reads_qc.types._format import CutadaptLogsDirectoryFormat, CutadaptLogsFmt
from q2_long_reads_qc.types._type import CutadaptLogs

citations = Citations.load("citations.bib", package="q2_long_reads_qc")

plugin = Plugin(
    name="long_reads_qc",
    version=__version__,
    website="https://github.com/bokulich-lab/q2-long-reads-qc",
    package="q2_long_reads_qc",
    description=(
        "QIIME2 plugin utilizing FastQC and MultiQC for comprehensive quality "
        "control analysis of 16S sequences, generating easy-to-interpret "
        "reports as QIIME2 vizualization."
    ),
    short_description="QIIME2 plugin for quality control of long sequences.",
)

plugin.register_formats(CutadaptLogsDirectoryFormat, CutadaptLogsFmt)
plugin.register_semantic_types(CutadaptLogs)
plugin.register_semantic_type_to_format(
    CutadaptLogs, artifact_format=CutadaptLogsDirectoryFormat
)

"""
plugin.visualizers.register_function(
    function=q2_long_reads_qc.fastMultiQC_stats,
    inputs={
        "sequences": SampleData[SequencesWithQuality | PairedEndSequencesWithQuality],
        "cutadapt_reports": CutadaptLogs,
    },
    parameters="",
    input_descriptions={
        "sequences": "Fastq input sequences.",
        "cutadapt_reports": "Cutadapt reports.",
    },
    parameter_descriptions={},
    name="Quality control statistics using FastQC and MultiQC.",
    description="Quality control statistics using FastQC and MultiQC.",
    citations=[citations["MultiQC"]],
)
"""

plugin.visualizers.register_function(
    function=q2_long_reads_qc.stats,
    inputs={
        "sequences": SampleData[SequencesWithQuality | PairedEndSequencesWithQuality],
    },
    parameters="",
    input_descriptions={
        "sequences": "Fastq input sequences.",
    },
    parameter_descriptions={},
    name="Quality control statistics using NanoPlot.",
    description="Quality control statistics using NanoPlot.",
    citations=[citations["Nanopack2"]],
)

plugin.methods.register_function(
    function=q2_long_reads_qc.chop,
    inputs={
        "query_reads": SampleData[SequencesWithQuality],
    },
    outputs=[("filtered_query_reads", SampleData[SequencesWithQuality])],
    parameters={
        "threads": Int % Range(1, None),
        "quality": Int % Range(0, None),
        "maxqual": Int % Range(0, None),
        "minlength": Int % Range(1, None),
        "maxlength": Int % Range(1, None),
        "headcrop": Int % Range(0, None),
        "tailcrop": Int % Range(0, None),
    },
    input_descriptions={
        "query_reads": "Fastq input sequences.",
    },
    output_descriptions={
        "filtered_query_reads": "The resulting filtered sequences.",
    },
    parameter_descriptions={
        "threads": "Number of threads.",
        "quality": "Sets a minimum Phred average quality score.",
        "maxqual": "Sets a maximum Phred average quality score.",
        "minlength": "Sets a minimum read length.",
        "maxlength": "Sets a maximum read length.",
        "headcrop": "Trim N nucleotides from the start of a read.",
        "tailcrop": "Trim N nucleotides from the end of a read.",
    },
    name="Filtering and trimming long reads using Chopper.",
    description="Filtering and trimming long reads using Chopper.",
    citations=[citations["Nanopack2"]],
)
